from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SqlEnum

from consts import PlatfromsTypeEnum
from database.db import Base


class BaseInfo(Base):
    __tablename__ = "base_info"
    info_id = Column(Integer, primary_key=True)
    sync_type = Column(SqlEnum(PlatfromsTypeEnum), nullable=False)


class TelegramInfo(Base):
    __tablename__ = "telegram_info"
    tel_info_id = Column(Integer, primary_key=True)
    token = Column(String)
    channel_id = Column(String)


class GithubInfo(Base):
    __tablename__ = "github_info"
    github_info_id = Column(Integer, primary_key=True)
    token = Column(String)
    repo_owner = Column(String)
    repo_name = Column(String)


class GoogleDriveInfo(Base):
    __tablename__ = "gdrive_info"
    gdrive_info_id = Column(Integer, primary_key=True)
    credentials_json = Column(String)
    target_folder = Column(String)
