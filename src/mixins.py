from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func

date_column_filler = mapped_column(DateTime(timezone=True), default=datetime.utcnow())


class TimeMixin:
    created: Mapped[datetime] = date_column_filler
    updated: Mapped[datetime] = date_column_filler
