from datetime import datetime
import pytz


def utc_now():
    # datetime.now() 不带时区信息
    return datetime.now().replace(tzinfo=pytz.utc)
