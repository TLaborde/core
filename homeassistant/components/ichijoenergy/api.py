"""Stub API for Ichijo Energy."""

import asyncio
import random


class IchijoEnergyApi:
    """Stub API for Ichijo Energy."""

    def __init__(self, host: str, username: str, password: str) -> None:
        """Initialize the API."""
        self.host = host
        self.username = username
        self.password = password

    async def authenticate(self) -> bool:
        """Simulate authentication."""
        # Simulate a network delay
        await asyncio.sleep(1)
        # Always return True for the stub
        return True

    async def get_data(self) -> dict:
        """Get random data for energy consumption, battery state, and solar output."""
        # Simulate a network delay
        await asyncio.sleep(2)

        return {
            "energy_consumption": round(random.uniform(0, 5000), 2),  # Watts
            "battery_state": round(random.uniform(0, 100), 1),  # Percentage
            "solar_output": round(random.uniform(0, 3000), 2),  # Watts
        }

    async def close(self) -> None:
        """Close the connection."""
        # No actual connection to close in the stub
