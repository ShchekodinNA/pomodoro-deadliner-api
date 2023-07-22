from datetime import datetime, timezone
from dateutil.tz import tzutc
from pydantic import BaseModel, Field
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func


def get_aware_utc_time_now():
    unaware_time = datetime.utcnow()
    aware_time = unaware_time.replace(tzinfo=timezone.utc)
    return aware_time


date_column_filler = mapped_column(DateTime(timezone=True), default=datetime.utcnow())
field_datetime = Field(default=get_aware_utc_time_now())


class TimeMixin:
    created: Mapped[datetime] = date_column_filler
    updated: Mapped[datetime] = date_column_filler


class TimeMixinForSchema(BaseModel):
    created: datetime | None = None
    updated: datetime | None = None

    def _init_private_attributes(self) -> None:
        self.created = (
            get_aware_utc_time_now() if self.created is None else self.created
        )
        self.updated = (
            get_aware_utc_time_now() if self.updated is None else self.updated
        )
