from pydantic import BaseModel, EmailStr, field_validator
import re


class RequestOtpSchema(BaseModel):
    """Step 1 — User supplies email; backend sends OTP to their phone."""
    email: EmailStr


class VerifyOtpSchema(BaseModel):
    """
    Step 2 — User submits the OTP they received.
    Returns a short-lived reset_token on success.
    """
    email: EmailStr
    otp_code: str


class ResetPasswordSchema(BaseModel):
    """Step 3 — User submits new password along with the reset_token."""
    email: EmailStr
    reset_token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit.")
        return v


class OtpResponseSchema(BaseModel):
    """Generic success/info response for OTP endpoints."""
    message: str
    # Only populated after successful OTP verification (step 2)
    reset_token: str | None = None
