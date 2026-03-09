from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base




class Point(Base):
    __tablename__ = "points"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    value: Mapped[int] = mapped_column(default=1)
    
    # You need TWO foreign keys because there are TWO people involved
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    issuer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Explicitly link them using foreign_keys to avoid ambiguity
    recipient: Mapped["User"] = relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="points"
    )
    issued_by: Mapped["User"] = relationship(
        "User",
        foreign_keys=[issuer_id],
        back_populates="points_issued"
    )
