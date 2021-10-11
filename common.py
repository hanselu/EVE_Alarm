import time


def get_ts() -> int:
    return time.time()


def cal_dt(ts: int) -> int:
    return get_ts() - ts


def str_to_ts(time_str: str) -> int:
    timeArray = time.strptime(time_str, r'%Y.%m.%d %H:%M:%S')
    return int(time.mktime(timeArray))


def ts_to_str(ts: int) -> str:
    return time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime(ts))


def ts_to_str_format(ts: int) -> str:
    dt = cal_dt(ts)
    if dt < 60:
        # return f'{int(dt)}秒'
        return f'刚刚'
    elif dt < 3600:
        return f'{int(dt//60)}分'
    elif dt < 86400:
        h = int(dt // 3600)
        m = int((dt % 3600) // 60)
        return f'{h}小时{m}分'
    else:
        return time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime(ts))
