from datetime import UTC, datetime, timedelta
from typing import Any

import jwt


class JWTService:
    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        issuer: str,
        audience: str,
        access_token_ttl_minutes: int,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.issuer = issuer
        self.audience = audience
        self.access_token_ttl_minutes = access_token_ttl_minutes

    def create_access_token(
        self,
        *,
        user_id: str,
        organization_id: str,
    ) -> str:
        now = datetime.now(UTC)
        expires_at = now + timedelta(
            minutes=self.access_token_ttl_minutes,
        )
        payload: dict[str, Any] = {
            "sub": user_id,
            "org": organization_id,
            "type": "access",
            "iss": self.issuer,
            "aud": self.audience,
            "iat": now,
            "exp": expires_at,
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            issuer=self.issuer,
            audience=self.audience,
            options={
                "require": [
                    "sub",
                    "org",
                    "type",
                    "iss",
                    "aud",
                    "iat",
                    "exp",
                ],
            },
        )
