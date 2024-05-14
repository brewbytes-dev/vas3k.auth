import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, BigInteger, MetaData
from sqlalchemy.orm import DeclarativeBase


bigint = Annotated[int, "bigint"]
my_metadata = MetaData()


class Base(DeclarativeBase):
    metadata = my_metadata
    type_annotation_map = {
        bigint: BigInteger,
        int: BigInteger,
        datetime.datetime: TIMESTAMP(timezone=True),
    }
