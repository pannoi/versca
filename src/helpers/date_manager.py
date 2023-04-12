from datetime import datetime
import pytz

def now_as_string() -> str:
    """
    Creates datetime as string

    Returns:
        str: Generated datetime.now() as string in propper format (UTC)
    """
    now = datetime.now(pytz.UTC)
    return now.strftime("%d/%m/%Y %H:%M:%S")
