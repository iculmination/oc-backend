from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload

from app.db.models.card import Card
from app.db.models.event import Event
from app.db.models.game import Game
from app.db.models.game_card import GameCard
from app.db.models.game_event import GameEvent
from app.db.models.game_log import GameLog
from app.db.models.player import Player
from app.engine.events.registry import EVENTS_REGISTRY
from app.engine.game_engine import GameEngine
from app.engine.mock.cards import draft_random_cards
from app.engine.state.card import CardState
from app.engine.state.game import GameState
from app.engine.state.player import PlayerState
from app.engine.utils.unit_of_work import UnitOfWork
from app.enums.event import EventRarity, EventSource, EventStatus, Events
from app.enums.game import GameStatus
from app.enums.player import PlayerRole, PlayerStatus
from app.schemas.game import (
    GameCardState,
    GameEventState,
    GameListResponse,
    GameLogEntry,
    GamePlayerState,
    GameSnapshot,
    GameStartResponse,
    GameStateResponse,
    GameSummary,
)


class GameRuntimeService:
    EVENT_CLASS_TO_EFFECT = {
        "BloodRainEvent": str(Events.BLOOD_RAIN),
        "PlagueEvent": str(Events.PLAGUE),
        "SolarFlareEvent": str(Events.SOLAR_FLARE),
    }

    def __init__(self):
        self._engine = GameEngine()

    def _serialize_state(self, state: GameState) -> GameSnapshot:
        return GameSnapshot(
            status=str(state.status),
            turn=state.turn,
            active_player=state.active_player,
            winner_id=state.winner_id,
            active_events=[
                GameEventState(name=event.__class__.__name__, duration=event.duration)
                for event in state.active_events
            ],
            players={
                player_id: GamePlayerState(
                    cards_alive=len([card for card in player.board if card.is_alive()]),
                    cards=[
                        GameCardState(
                            id=card.id,
                            name=card.name,
                            health=card.health,
                            max_health=card.max_health,
                            attack=card.attack,
                            ability=str(card.ability),
                            statuses=[str(status) for status in card.statuses],
                            last_action=card.last_action,
                        )
                        for card in player.board
                    ],
                )
                for player_id, player in state.players.items()
            },
            battle_log=[
                GameLogEntry(round=entry["round"], actor=entry["actor"], text=entry["text"])
                for entry in state.battle_log
            ],
        )

    def _append_log(self, state: GameState, round_number: int, actor: str, text: str):
        state.battle_log.append({"round": round_number, "actor": actor, "text": text})

    def _get_player_and_bot(self, players: list[Player], user_id: UUID) -> tuple[Player, Player]:
        player_by_user = next(
            (player for player in players if player.user_id == user_id and not player.is_bot),
            None,
        )
        if not player_by_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a participant of this game",
            )

        bot_player = next((player for player in players if player.is_bot), None)
        if not bot_player:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bot player is missing",
            )

        return player_by_user, bot_player

    async def _ensure_event_definitions(self, uow: UnitOfWork) -> dict[str, Event]:
        by_effect: dict[str, Event] = {}
        for event_key in EVENTS_REGISTRY.keys():
            existing = await uow.session.scalar(
                select(Event).where(Event.effect == str(event_key))
            )
            if existing:
                by_effect[str(event_key)] = existing
                continue
            created = Event(
                name=str(event_key).replace("_", " ").title(),
                rarity=EventRarity.COMMON,
                status=EventStatus.ONGOING,
                source=EventSource.RANDOM,
                effect=str(event_key),
                description=f"Auto-created definition for {event_key}",
                is_active=True,
            )
            uow.session.add(created)
            await uow.session.flush()
            by_effect[str(event_key)] = created
        return by_effect

    async def _load_game_bundle(self, uow: UnitOfWork, game_id: UUID):
        game = await uow.session.scalar(select(Game).where(Game.id == game_id))
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        players = (
            await uow.session.scalars(
                select(Player).where(Player.game_id == game_id).order_by(Player.seat.asc())
            )
        ).all()
        cards = (
            await uow.session.scalars(
                select(GameCard)
                .where(GameCard.game_id == game_id, GameCard.zone == "board")
                .options(selectinload(GameCard.card_definition))
            )
        ).all()
        game_events = (
            await uow.session.scalars(
                select(GameEvent).where(
                    GameEvent.game_id == game_id, GameEvent.status == EventStatus.ONGOING
                ).options(selectinload(GameEvent.event_definition))
            )
        ).all()
        logs = (
            await uow.session.scalars(
                select(GameLog)
                .where(GameLog.game_id == game_id)
                .order_by(GameLog.round_number.asc(), GameLog.sequence.asc())
            )
        ).all()
        return game, players, cards, game_events, logs

    def _build_state(
        self, game: Game, players: list[Player], cards: list[GameCard], game_events: list[GameEvent]
    ):
        if not players:
            raise HTTPException(status_code=409, detail="Game has no players")

        players_state: dict[UUID, PlayerState] = {}
        for player in players:
            players_state[player.id] = PlayerState(id=player.id)

        for game_card in cards:
            players_state[game_card.player_id].board.append(
                CardState(
                    id=game_card.id,
                    card_id=game_card.card_definition_id or game_card.id,
                    owner_id=game_card.player_id,
                    name=game_card.card_definition.name,
                    attack=game_card.attack_current,
                    health=game_card.health_current,
                    max_health=game_card.max_health_current,
                    ability=str(game_card.card_definition.ability),
                    nature=game_card.card_definition.nature,
                    statuses=game_card.statuses or [],
                    last_action=game_card.last_action,
                )
            )

        active_events = []
        for ge in game_events:
            event_key = Events(ge.event_definition.effect)
            event = EVENTS_REGISTRY[event_key](duration=ge.duration_left)
            active_events.append(event)

        active_player_id = game.turn_player_id or players[0].id
        winner_id = game.winner_player_id

        return GameState(
            id=game.id,
            turn=game.turn,
            active_player=active_player_id,
            players=players_state,
            active_events=active_events,
            status=game.status,
            winner_id=winner_id,
        )

    async def _persist_state(
        self,
        uow: UnitOfWork,
        game: Game,
        state: GameState,
        cards: list[GameCard],
        event_by_effect: dict[str, Event],
        new_log_entries: list[dict],
    ):
        card_by_id = {card.id: card for card in cards}
        for player_state in state.players.values():
            for card_state in player_state.board:
                db_card = card_by_id.get(card_state.id)
                if not db_card:
                    continue
                db_card.attack_current = card_state.attack
                db_card.health_current = card_state.health
                db_card.max_health_current = card_state.max_health
                db_card.is_alive = card_state.is_alive()
                db_card.statuses = [str(status) for status in card_state.statuses]
                db_card.last_action = card_state.last_action

        game.turn = state.turn
        game.status = state.status
        game.turn_player_id = state.active_player
        game.winner_player_id = state.winner_id
        game.state_snapshot = self._serialize_state(state).model_dump(mode="json")

        await uow.session.execute(delete(GameEvent).where(GameEvent.game_id == game.id))
        for event in state.active_events:
            effect_key = self.EVENT_CLASS_TO_EFFECT.get(event.__class__.__name__)
            if not effect_key:
                continue
            event_def = event_by_effect.get(effect_key)
            if not event_def:
                continue
            uow.session.add(
                GameEvent(
                    game_id=game.id,
                    event_id=event_def.id,
                    duration_left=event.duration,
                    applied_at_round=state.turn,
                    status=EventStatus.ONGOING,
                )
            )

        existing_logs_count = await uow.session.scalar(
            select(func.count(GameLog.id)).where(GameLog.game_id == game.id)
        )
        sequence_start = existing_logs_count or 0
        for index, entry in enumerate(new_log_entries):
            uow.session.add(
                GameLog(
                    game_id=game.id,
                    round_number=entry["round"],
                    sequence=sequence_start + index + 1,
                    actor_type=entry["actor"],
                    action_type="round_event",
                    message=entry["text"],
                    payload=entry,
                )
            )

    def _choose_bot_action(self, state: GameState, bot_id: UUID):
        bot_player = state.players[bot_id]
        alive_cards = [card for card in bot_player.board if card.is_alive()]
        if not alive_cards:
            return None, None
        chosen = alive_cards[0]
        target_id = None

        if str(chosen.ability) == "attack":
            enemies = []
            for pid, player in state.players.items():
                if pid == bot_id:
                    continue
                enemies.extend([card for card in player.board if card.is_alive()])
            if enemies:
                target_id = enemies[0].id

        if str(chosen.ability) in ["heal", "buff"]:
            allies = [card for card in bot_player.board if card.is_alive()]
            if allies:
                target_id = allies[0].id

        return chosen.id, target_id

    async def start_vs_bot(self, user_id: UUID) -> GameStartResponse:
        async with UnitOfWork() as uow:
            event_by_effect = await self._ensure_event_definitions(uow)

            existing_active_game = await uow.session.scalar(
                select(Game)
                .join(Player, Player.game_id == Game.id)
                .where(
                    Player.user_id == user_id,
                    Player.is_bot.is_(False),
                    Game.status == GameStatus.ONGOING,
                )
                .order_by(Game.updated_at.desc())
            )
            if existing_active_game:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User already has an active game: {existing_active_game.id}",
                )

            game = Game(turn=0, status=GameStatus.ONGOING)
            uow.session.add(game)
            await uow.session.flush()

            player = Player(
                game_id=game.id,
                user_id=user_id,
                is_bot=False,
                seat=1,
                display_name="Player",
                role=PlayerRole.HOST,
                status=PlayerStatus.CONNECTED,
            )
            bot = Player(
                game_id=game.id,
                user_id=None,
                is_bot=True,
                seat=2,
                display_name="Bot",
                role=PlayerRole.GUEST,
                status=PlayerStatus.CONNECTED,
            )
            uow.session.add_all([player, bot])
            await uow.session.flush()

            game.turn_player_id = player.id

            player_cards = draft_random_cards(player.id, count=4)
            bot_cards = draft_random_cards(bot.id, count=4)
            all_cards = [*player_cards, *bot_cards]

            for card in all_cards:
                card_definition = Card(
                    id=card.card_id,
                    name=card.name,
                    max_health=card.max_health,
                    attack=card.attack,
                    ability=card.ability,
                    nature=card.nature,
                )
                uow.session.add(card_definition)
                uow.session.add(
                    GameCard(
                        id=card.id,
                        game_id=game.id,
                        player_id=card.owner_id,
                        card_definition_id=card.card_id,
                        zone="board",
                        attack_current=card.attack,
                        health_current=card.health,
                        max_health_current=card.max_health,
                        is_alive=card.is_alive(),
                        statuses=[str(status) for status in card.statuses],
                        last_action=card.last_action,
                    )
                )

            await uow.session.flush()

            game_db, players_db, cards_db, game_events_db, logs_db = await self._load_game_bundle(
                uow, game.id
            )
            state = self._build_state(game_db, players_db, cards_db, game_events_db)
            state.battle_log = [
                {"round": log.round_number, "actor": log.actor_type, "text": log.message}
                for log in logs_db
            ]

            game.state_snapshot = self._serialize_state(state).model_dump(mode="json")
            return GameStartResponse(
                game_id=game.id,
                player_id=player.id,
                bot_id=bot.id,
                state=self._serialize_state(state),
            )

    async def play_turn(
        self, game_id: UUID, user_id: UUID, card_id: UUID, target_id: UUID | None
    ) -> GameStateResponse:
        async with UnitOfWork() as uow:
            event_by_effect = await self._ensure_event_definitions(uow)
            game, players, cards, game_events, logs = await self._load_game_bundle(uow, game_id)

            player_by_user, bot_player = self._get_player_and_bot(players, user_id)

            state = self._build_state(game, players, cards, game_events)
            state.battle_log = [
                {"round": log.round_number, "actor": log.actor_type, "text": log.message}
                for log in logs
            ]

            if state.status == GameStatus.FINISHED:
                return GameStateResponse(game_id=game_id, state=self._serialize_state(state))

            if state.active_player != player_by_user.id:
                raise HTTPException(status_code=409, detail="Not player's turn")

            round_number = state.turn + 1
            existing_logs_len = len(state.battle_log)
            self._append_log(state, round_number, "system", f"Round {round_number} started.")
            self._engine.events_phase(state)
            if state.active_events:
                active_events_text = ", ".join(
                    f"{event.__class__.__name__}({event.duration})" for event in state.active_events
                )
                self._append_log(
                    state, round_number, "system", f"Active events: {active_events_text}"
                )
            else:
                self._append_log(state, round_number, "system", "No active events this round.")

            for player in state.players.values():
                for card in player.board:
                    card.last_action = None

            player_action_text = self._engine.play_selected_action(
                state, card_id=card_id, target_id=target_id
            )
            self._append_log(state, round_number, "player", player_action_text)

            if state.status != GameStatus.FINISHED and state.active_player == bot_player.id:
                bot_card_id, bot_target_id = self._choose_bot_action(state, bot_player.id)
                if bot_card_id is not None:
                    bot_action_text = self._engine.play_selected_action(
                        state, card_id=bot_card_id, target_id=bot_target_id
                    )
                    self._append_log(state, round_number, "bot", bot_action_text)
                else:
                    self._append_log(state, round_number, "bot", "No alive cards to act.")

            if state.status == GameStatus.FINISHED:
                if state.winner_id is None:
                    self._append_log(state, round_number, "system", "Game finished in a draw.")
                elif state.winner_id == player_by_user.id:
                    self._append_log(state, round_number, "system", "Game finished. Player wins.")
                elif state.winner_id == bot_player.id:
                    self._append_log(state, round_number, "system", "Game finished. Bot wins.")
                else:
                    self._append_log(state, round_number, "system", "Game finished.")

            state.turn = round_number

            new_log_entries = state.battle_log[existing_logs_len:]
            await self._persist_state(
                uow=uow,
                game=game,
                state=state,
                cards=cards,
                event_by_effect=event_by_effect,
                new_log_entries=new_log_entries,
            )

            return GameStateResponse(
                game_id=game_id,
                player_id=player_by_user.id,
                bot_id=bot_player.id,
                state=self._serialize_state(state),
            )

    async def get_state(self, game_id: UUID, user_id: UUID) -> GameStateResponse:
        async with UnitOfWork() as uow:
            game, players, cards, game_events, logs = await self._load_game_bundle(uow, game_id)
            player_by_user, bot_player = self._get_player_and_bot(players, user_id)

            state = self._build_state(game, players, cards, game_events)
            state.battle_log = [
                {"round": log.round_number, "actor": log.actor_type, "text": log.message}
                for log in logs
            ]
            return GameStateResponse(
                game_id=game_id,
                player_id=player_by_user.id,
                bot_id=bot_player.id,
                state=self._serialize_state(state),
            )

    async def get_active_game(self, user_id: UUID) -> GameSummary | None:
        async with UnitOfWork() as uow:
            game = await uow.session.scalar(
                select(Game)
                .join(Player, Player.game_id == Game.id)
                .where(
                    Player.user_id == user_id,
                    Player.is_bot.is_(False),
                    Game.status == GameStatus.ONGOING,
                )
                .order_by(Game.updated_at.desc())
            )
            if not game:
                return None

            return GameSummary(
                game_id=game.id,
                status=str(game.status),
                turn=game.turn,
                winner_player_id=game.winner_player_id,
                updated_at=game.updated_at.isoformat(),
            )

    async def list_games(self, user_id: UUID) -> GameListResponse:
        async with UnitOfWork() as uow:
            games = (
                await uow.session.scalars(
                    select(Game)
                    .join(Player, Player.game_id == Game.id)
                    .where(Player.user_id == user_id, Player.is_bot.is_(False))
                    .order_by(Game.updated_at.desc())
                )
            ).all()

            return GameListResponse(
                games=[
                    GameSummary(
                        game_id=game.id,
                        status=str(game.status),
                        turn=game.turn,
                        winner_player_id=game.winner_player_id,
                        updated_at=game.updated_at.isoformat(),
                    )
                    for game in games
                ]
            )

    async def _finish_game_for_user(
        self, game_id: UUID, user_id: UUID, *, surrender: bool
    ) -> GameStateResponse:
        async with UnitOfWork() as uow:
            game, players, cards, game_events, logs = await self._load_game_bundle(uow, game_id)
            player_by_user, bot_player = self._get_player_and_bot(players, user_id)
            state = self._build_state(game, players, cards, game_events)
            state.battle_log = [
                {"round": log.round_number, "actor": log.actor_type, "text": log.message}
                for log in logs
            ]

            if state.status != GameStatus.FINISHED:
                state.status = GameStatus.FINISHED
                state.winner_id = bot_player.id if surrender else None
                state.turn += 1
                message = (
                    "Player surrendered. Bot wins."
                    if surrender
                    else "Game was ended manually by player."
                )
                self._append_log(state, state.turn, "system", message)
                new_log_entries = [state.battle_log[-1]]
                await self._persist_state(
                    uow=uow,
                    game=game,
                    state=state,
                    cards=cards,
                    event_by_effect=await self._ensure_event_definitions(uow),
                    new_log_entries=new_log_entries,
                )

            return GameStateResponse(
                game_id=game_id,
                player_id=player_by_user.id,
                bot_id=bot_player.id,
                state=self._serialize_state(state),
            )

    async def surrender(self, game_id: UUID, user_id: UUID) -> GameStateResponse:
        return await self._finish_game_for_user(game_id, user_id, surrender=True)

    async def end_game(self, game_id: UUID, user_id: UUID) -> GameStateResponse:
        return await self._finish_game_for_user(game_id, user_id, surrender=False)


game_runtime_service = GameRuntimeService()
