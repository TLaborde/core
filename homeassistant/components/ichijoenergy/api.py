"""retrieve data from network."""

import base64
import json
import os

import aiohttp
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import requests

# from .const import LOGGER


class IchijoEnergyAPI:
    """do the magic."""

    URL = "http://172.19.19.254/wui/api/sm_api.php"

    def __init__(self) -> None:
        "Get basic values."

    @staticmethod
    def discover() -> bool:
        """Check if the service is available on the network."""
        try:
            response = requests.get(IchijoEnergyAPI.URL, timeout=3)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            # LOGGER.exception(err)
            pass
        return False

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
        async with (
            aiohttp.ClientSession() as session,
            session.post(IchijoEnergyAPI.URL, data=json.dumps(enc)) as resp,
        ):
            r = await resp.text()
        answer = json.loads(r)
        dec = AESCipher.decrypt(answer["p1"], answer["p2"])
        return IchijoEnergyOutputData(dec)


class IchijoEnergyOutputData:
    """do the magic."""

    def __init__(self, result: str) -> None:
        """Set basic format."""
        data = json.loads(result)
        data = data["res_data"]["data"]

        # solar
        self.power_production = float(
            data["current"]["Genaration"]  # codespell:ignore
        )
        self.energy_production_today = float(
            data["today"]["Genaration"]  # codespell:ignore
        )
        self.energy_production_month = float(
            data["month"]["Genaration"]  # codespell:ignore
        )  # codespell:ignore
        self.energy_production_total = float(
            data["lifetime"]["Genaration"]  # codespell:ignore
        )

        # sold to the grid
        self.power_export = float(data["current"]["Export"])
        self.energy_export_today = float(data["today"]["Export"])
        self.energy_export_month = float(data["month"]["Export"])
        self.energy_export_total = float(data["lifetime"]["Export"])

        # purchased from the grid
        self.power_import = float(data["current"]["Purchase"])
        self.energy_import_today = float(data["today"]["Purchase"])
        self.energy_import_month = float(data["month"]["Purchase"])
        self.energy_import_total = float(data["lifetime"]["Purchase"])

        # used
        self.power_consumption = float(data["current"]["Consumption"])
        self.energy_consumption_today = float(data["today"]["Consumption"])
        self.energy_consumption_month = float(data["month"]["Consumption"])
        self.energy_consumption_total = float(data["lifetime"]["Consumption"])

        # battery charge
        self.power_charge = float(data["current"]["Charge"])
        self.energy_power_charge_today = float(data["today"]["Charge"])
        self.energy_power_charge_month = float(data["month"]["Charge"])
        self.energy_power_charge_total = float(data["lifetime"]["Charge"])

        # battery discharge
        self.power_discharge = float(data["current"]["Discharge"])
        self.energy_power_discharge_today = float(data["today"]["Discharge"])
        self.energy_power_discharge_month = float(data["month"]["Discharge"])
        self.energy_power_discharge_total = float(data["lifetime"]["Discharge"])

        # real time solar panel performance ratio
        self.performance_ratio = float(data["current"]["PV_ratio"])

        self.self_sufficiency_today = float(data["today"]["self_sufficiency"])
        self.self_sufficiency_month = float(data["month"]["self_sufficiency"])
        self.self_sufficiency_total = float(data["lifetime"]["self_sufficiency"])

        self.battery_level = float(data["bat"]["SOC"])


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
        unpadder = PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
        return plaintext.decode("utf-8")


if __name__ == "__main__":
    import asyncio

    ie = IchijoEnergyAPI()
    res = asyncio.run(ie.get_output_data())
