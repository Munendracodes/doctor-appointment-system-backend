from pydantic import BaseModel, Field

class SendOtpRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)


class VerifyOtpRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    otp: str = Field(..., min_length=4, max_length=6)

