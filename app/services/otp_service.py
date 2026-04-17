from app.redis.client import redis_client
import random
import hmac
import hashlib

from app.core.security import create_access_token

SECRET_KEY = "super-secret-key"
OTP_EXPIRY = 300
COOLDOWN = 60
DAILY_LIMIT = 5
OTP_ATTEMPT_LIMIT = 5


def hash_otp(otp: str, phone: str) -> str:
    message = f"{otp}:{phone}"
    return hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


def generate_otp():
    return str(random.randint(1000, 9999))


async def send_otp(phone: str) -> dict:
    otp_key = f"otp:{phone}"
    cooldown_key = f"otp:cooldown:{phone}"
    daily_key = f"otp:daily:{phone}"
    attempts_key = f"otp:attempts:{phone}"

    if await redis_client.exists(cooldown_key):
        return {
            "status": 429,
            "message": f"OTP recently sent. Wait {COOLDOWN} seconds."
        }

    daily_count = await redis_client.incr(daily_key)
    if daily_count == 1:
        await redis_client.expire(daily_key, 86400)

    if daily_count > DAILY_LIMIT:
        return {
            "status": 429,
            "message": "Daily limit exceeded, try after 24 hours."
        }

    otp = generate_otp()
    hashed = hash_otp(otp, phone)

    await redis_client.set(otp_key, hashed, ex=OTP_EXPIRY)
    await redis_client.set(cooldown_key, 1, ex=COOLDOWN)
    await redis_client.delete(attempts_key)

    print(f"[DEBUG OTP] {phone} -> {otp}")

    return {
        "status": 200,
        "message": "OTP sent",
        "time_to_live_seconds": OTP_EXPIRY
    }


async def validate_otp(phone: str, otp: str, user_service) -> dict:
    otp_key = f"otp:{phone}"
    attempts_key = f"otp:attempts:{phone}"

    stored_hash = await redis_client.get(otp_key)

    if not stored_hash:
        return {"status": 400, "message": "OTP expired"}

    attempts = await redis_client.incr(attempts_key)
    if attempts == 1:
        await redis_client.expire(attempts_key, OTP_EXPIRY)

    if attempts > OTP_ATTEMPT_LIMIT:
        return {"status": 429, "message": "Max attempts exceeded, request new OTP."}

    is_valid = hmac.compare_digest(
        stored_hash,
        hash_otp(otp, phone)
    )

    if is_valid:
        await redis_client.delete(otp_key)
        await redis_client.delete(attempts_key)

        user = await user_service.get_or_create_user(phone)

        token = create_access_token({
            "sub": phone,
            "id": user.id,
            "role": user.role
        })

        return {
            "status": 200,
            "message": "OTP verified",
            "access_token": token,
            "token_type": "bearer"
        }

    return {
        "status": 400,
        "message": "Invalid OTP",
        "error_code": "INVALID_OTP",
        "attempts_left": OTP_ATTEMPT_LIMIT - attempts
    }