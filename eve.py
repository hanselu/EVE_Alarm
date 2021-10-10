import config
import esi
import log
from os import path, listdir

setting = config.get_config()


def _get_log_folder_path() -> str:
    if setting.LOG_PATH == '':
        # 自动获取目录
        pass
        log_path = path.expanduser('~\Documents\EVE\logs\Chatlogs')
        if path.exists(log_path):
            return log_path
        else:
            return None
    else:
        # 使用指定目录
        if path.exists(setting.LOG_PATH):
            return setting.LOG_PATH
        else:
            return None


def _get_log_file_name(listener_name: str = setting['listener'], keyword: str = setting['channel']) -> str:
    listener_id = esi.get_character_id(listener_name)
    folder_path = setting['log_path']
    if folder_path:
        # 获取预警频道文件并按时间排序
        file_list = sorted(listdir(folder_path), key=lambda fn: path.getmtime(
            path.join(folder_path, fn)), reverse=True)

        for fn in file_list:
            # id_flag = fn.find(str(listener_id))
            # keyword_flag = fn.find(keyword)

            # print(fn, id_flag, keyword_flag)
            if fn.find(str(listener_id)) > -1 and fn.find(keyword) > -1:
                return path.join(folder_path, fn)

    return None


def _get_alarm_log_file_name(listener_name: str = setting['listener']) -> str:
    return _get_log_file_name(listener_name, setting['channel'])


def _get_local_log_file_name(listener_name: str = setting['listener']) -> str:
    return _get_log_file_name(listener_name, '本地')


def get_local(listener_name: str = setting['listener']) -> str:
    """
    获取指定人物所在地
    """
    return log.get_local(_get_local_log_file_name(listener_name))


def get_alarm_list(location: str = None, listener_name: str = setting['listener'],
                   channel: str = setting['channel']) -> list:
    """
    返回预警信息
    """
    log_file = _get_alarm_log_file_name(listener_name)
    # alarm_list = log.get_alarm_list(log_file, setting['overtime'])

    # 根据设置，过滤预警
    new_list = []
    for a in log.get_alarm_list(log_file, setting['overtime'], location):
        if a.distance() <= setting['ignore_distance']:
            new_list.append(a)
        else:
            pass
            # print(f"{a.solar_system} {a.distance()} 跳 超过{setting['ignore_distance']}跳")

    return new_list


if __name__ == '__main__':
    print(_get_local_log_file_name('欠我10块'))
    print(_get_local_log_file_name())
    local = get_local()
    print(local)
    for a in get_alarm_list():
        print(a, esi.cal_route(local, a.solar_system))
