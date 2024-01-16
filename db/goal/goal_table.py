import os

from sqlalchemy import Integer, String, Float
from sqlalchemy.sql.schema import Column
from db.connection import Base, engine

from sqlalchemy_file import FileField

from libcloud.storage.drivers.local import LocalStorageDriver

from sqlalchemy_file.storage import StorageManager


class GoalTable(Base):
    __tablename__ = "goal"

    uuid = Column(String, primary_key=True)
    phase = Column(String, nullable=False)
    turn = Column(Integer, nullable=False)
    file = Column(FileField)
    predict = Column(String, nullable=False)
    max = Column(Integer, nullable=False)
    real = Column(Float, nullable=True)


# Configure Storage
os.makedirs("./upload_dir/goal", 0o777, exist_ok=True)
container = LocalStorageDriver("./upload_dir").get_container("goal")
StorageManager.add_storage("default", container)

Base.metadata.create_all(engine)
