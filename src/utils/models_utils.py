from datetime import datetime
from zoneinfo import ZoneInfo

timezone = ZoneInfo("America/Sao_Paulo")


def obter_data_atual() -> datetime:
    return datetime.now(tz=timezone).replace(tzinfo=None)
