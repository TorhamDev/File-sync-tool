from sqlalchemy.orm import Session

from database.models import TelegramInfo


class TelegramRepository:
    def __init__(self, session: Session) -> None:
        self.session = session


    def get_last(self) -> TelegramInfo | None:
        return self.session.query(TelegramInfo).order_by(TelegramInfo.id.desc()).first()

    def get_telegram_info_by_channel_id(self, channel_id: str) -> TelegramInfo:
        query = self.session.query(TelegramInfo).where(
            TelegramInfo.channel_id == channel_id
        )
        return query.scalar()

    def create_telegram_info(self, token: str, channel_id: str) -> TelegramInfo:
        query = TelegramInfo(token=token, channel_id=channel_id)
        self.session.add(query)
        return self.get_telegram_info_by_channel_id(channel_id=channel_id)
