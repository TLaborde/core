"""retrieve data from network."""

import base64
import json
import os

import aiohttp
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


class IchijoEnergyAPI:
    """do the magic."""

    URL = "http://172.19.19.254/wui/api/sm_api.php"

    def __init__(self) -> None:
        "Get basic values."

    async def get_output_data(self):
        """Retrieve data from network."""
        payload = {
            "id": "usBDG07249",
            "pass": "acc04fef4",
            "cmd": "current_data",
            "req_data": "",
        }
        stringify = json.dumps(payload)
        enc = AESCipher.encrypt(stringify)
        async with aiohttp.ClientSession().post(
            IchijoEnergyAPI.URL, data=json.dumps(enc)
        ) as resp:
            r = await resp.text()
        answer = json.loads(r)
        dec = AESCipher.decrypt(answer["p1"], answer["p2"])
        return IchijoEnergyOutputData(dec)


class IchijoEnergyOutputData:
    """do the magic."""

    def __init__(self, result: str) -> None:
        """Set basic format."""
        data = json.loads(result)
        current_generation = float(
            data["res_data"]["current"]["Genaration"]  # codespell:ignore
        )
        current_export = float(data["res_data"]["current"]["Export"])
        current_purchase = float(data["res_data"]["current"]["Purchase"])
        current_consumption = float(data["res_data"]["current"]["Consumption"])
        current_charge = float(data["res_data"]["current"]["Charge"])
        current_discharge = float(data["res_data"]["current"]["Discharge"])
        if current_charge > 0:
            self.battery = current_charge
        else:
            self.battery = -current_discharge
        if current_export > 0:
            self.grid = current_export
        else:
            self.grid = current_purchase
        self.home = current_consumption
        self.solar = current_generation


class AESCipher:
    """Encrypts and decrypts payload."""

    key = b"B\xb8\x9a\xc5\x9e\xdb+\xde\x15\xe3,>%\xae\xbaY"

    @staticmethod
    def encrypt(raw: str) -> dict:
        """Encrypt raw data."""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(AESCipher.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded_bytes = padder.update(bytes(raw, "utf-8"))
        padded_bytes += padder.finalize()
        encrypted_bytes = encryptor.update(padded_bytes)

        return {
            "p1": base64.b64encode(encrypted_bytes).decode("utf-8"),
            "p2": base64.b64encode(iv).decode("utf-8"),
        }

    @staticmethod
    def decrypt(enc, iv):
        """Decrypt payload."""
        decodedciphertext = base64.b64decode(enc)
        iv = base64.b64decode(iv)
        cipher = Cipher(algorithms.AES(AESCipher.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(decodedciphertext) + decryptor.finalize()
        unpadder = PKCS7(16).unpadder()
        plaintext = unpadder.update(padded_data)
        return plaintext.decode("utf-8")
