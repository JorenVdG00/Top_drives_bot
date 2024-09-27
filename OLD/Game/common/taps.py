import random
import time

from OLD.Game.common.base import tap

from config import resize_values, SLEEP_TIME_A
from OLD.Utils.resize_utils import resize_ranges







def tap_clubs(time_sleep=SLEEP_TIME_A):
    x1, x2, y1, y2 = resize_ranges(260, 520, 500, 750, resize_values)
    x, y = random.randint(x1, x2), random.randint(y1, y2)
    tap(x, y)
    time.sleep(time_sleep)
