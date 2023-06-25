from typing import Optional
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from passlib.context import CryptContext
from jose import jwt


class SecretController:
    def __init__(self, hashing_schema: str, 
                 encypting_alg: str,
                 jwt_secret: str, 
                 pepper_secret: str) -> None:
        self._hashing_schema: str = hashing_schema
        self._encypting_alg: str = encypting_alg
        self._jwt_secret: str = jwt_secret
        self._pepper_secret: str = pepper_secret
        self.pwd_context = CryptContext(
            schemes=[self._hashing_schema], deprecated="auto"
        )

    def is_secret_correct(self, hashed_secret: str, secret_to_check: str) -> bool:
        peppered_password = self.pepper_secret_by_bcrypt(secret_to_check)
        return self.pwd_context.verify(peppered_password, hashed_secret)

    def generate_jwt_token(
        self, body: dict, expires_delta: timedelta = timedelta(minutes=15)
    ) -> str:
        body_to_encode = body.copy()
        expire = datetime.utcnow() + expires_delta
        body_to_encode.update({"exp": expire})
        jwt_token = jwt.encode(
            body_to_encode,
            self._jwt_secret,
            algorithm=self._encypting_alg,
        )
        return jwt_token

    def pepper_secret_by_bcrypt(self, secret: str) -> str:
        return bcrypt.using(salt=self._pepper_secret).hash(secret)

    def hash_secret(self, secret: str) -> str:
        peppered_secret = self.pepper_secret_by_bcrypt(secret)
        hashed_secret = self.pwd_context.hash(peppered_secret)
        return hashed_secret
