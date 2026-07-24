from sqlalchemy.orm import Session

from consts import PlatfromsTypeEnum
from database.models import BaseInfo


class BaseInfoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def base_info_exists(self) -> bool:
        query = self.session.query(BaseInfo).order_by(BaseInfo.id.desc())
        return self.session.query(query.exists()).scalar()

    def get_last(self) -> BaseInfo | None:
        return self.session.query(BaseInfo).order_by(BaseInfo.id.desc()).first()

    def create_base_info(self, sync_type: PlatfromsTypeEnum, sync_dir: str) -> BaseInfo:
        query = BaseInfo(sync_type=sync_type, sync_dir=sync_dir)
        self.session.add(query)
        return self.get_last()
