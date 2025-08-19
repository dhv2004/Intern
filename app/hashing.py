from passlib.context import CryptContext
from Crypto.Cipher import AES
import os
import base64

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    secret_key = b'.6\x87\xed\xb0\x86&u\xfbzWM\x06\xf8\x93\xdeE&\n\xd9\xa9W4\x8a\xb3M\x9ez\xb7L\x08\x9e'

    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)

    @staticmethod
    def encrypt_password(password: str) -> str:
        iv = os.urandom(AES.block_size)
        cipher = AES.new(Hash.secret_key, AES.MODE_CFB, iv)
        enc = iv + cipher.encrypt(password.encode())
        return base64.b64encode(enc).decode('utf-8')

    @staticmethod
    def decrypt_password(encrypt_password: str) -> str:
        encrypted_data = base64.b64decode(encrypt_password)
        iv = encrypted_data[:AES.block_size]
        cipher = AES.new(Hash.secret_key, AES.MODE_CFB, iv)
        decrypted = cipher.decrypt(encrypted_data[AES.block_size:])
        return decrypted.decode('utf-8')
