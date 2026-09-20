from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.base import Base

if TYPE_CHECKING:
    from api.models.transaction import Transaction


class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alert_reference: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id"),
        nullable=False,
    )
    alert_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    transaction: Mapped["Transaction"] = relationship(
        back_populates="fraud_alerts",
    )