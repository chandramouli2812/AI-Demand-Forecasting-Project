from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from fastapi_app.db.session import Base


class OtpRecord(Base):
    __tablename__ = "otp_records"

    id = Column(Integer, primary_key=True, index=True)

    # The phone number OTP was sent to
    phone_number = Column(String(20), nullable=False, index=True)

    # The 6-digit OTP (stored as plain string; short-lived)
    otp_code = Column(String(10), nullable=False)

    # Which user this OTP belongs to (via email lookup)
    user_email = Column(String(255), nullable=False, index=True)

    # Has this OTP been used already?
    is_used = Column(Boolean, default=False, nullable=False)

    # When this OTP expires (typically now + 10 minutes)
    expires_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return (
            f"<OtpRecord(id={self.id}, phone={self.phone_number}, "
            f"email={self.user_email}, used={self.is_used})>"
        )
