"""retrieve data from network."""


class IchijoEnergyAPI:
    """do the magic."""

    URL = "http://172.19.19.254/wui/app/login.php"

    def __init__(self) -> None:
        "Get basic values."

    async def get_output_data(self):
        """Retrieve data from network."""
        # mock return for now
        return IchijoEnergyOutputData()


class IchijoEnergyOutputData:
    """do the magic."""

    def __init__(self) -> None:
        """Set basic format."""
        self.battery = 12
        self.grid = 0
        self.home = 2
        self.solar = 5
