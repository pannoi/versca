import pytest
import pytz
from datetime import datetime

from context import date_manager

def test_now_as_string():
    now_as_string = date_manager.now_as_string()
    now_as_datetime = datetime.strptime(now_as_string, "%d/%m/%Y %H:%M:%S")
    now = datetime.now(pytz.UTC)
    now = now.strftime("%d/%m/%Y %H:%M:%S")
    now = datetime.strptime(now, "%d/%m/%Y %H:%M:%S")

    assert now == now_as_datetime
