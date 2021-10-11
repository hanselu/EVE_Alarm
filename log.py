import re
from alarm import Alarm

load_local_file_count = 0
load_channel_file_count = 0


def get_local(log_file: str) -> str:
    """
    读取当前位置
    """
    # 统计读取本地频道文件次数
    global load_local_file_count
    load_local_file_count += 1
    print(f'读取本地频道{load_local_file_count}次')

    with open(log_file, 'r', encoding='utf16') as f:
        txt_list = f.readlines()

    local_list = []
    for line in txt_list:
        result = re.search(
            r'\[ (\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) ] EVE系统 > 频道更换为本地：(.*)', line)

        if result:
            local_list.append(result.group(2))

    if len(local_list) > 0:
        return local_list[-1]

    return '未知'


def get_alarm_list(log_file: str, overtime: int, location: str = None) -> list:
    # 统计读取预警频道文件次数
    global load_channel_file_count
    load_channel_file_count += 1
    print(f'读取预警频道{load_channel_file_count}次')

    with open(log_file, 'r', encoding='utf16') as f:
        txt_list = f.readlines()

    alarm_list = []
    for line in txt_list:
        alarm = Alarm(line, location)
        # 排除系统消息
        if alarm.speaker == 'EVE系统':
            continue
        if alarm.solar_system and alarm.dt < overtime:
            new_alarm = True
            for index, a in enumerate(alarm_list):
                if alarm.solar_system == a.solar_system:
                    alarm_list[index] = alarm
                    # print(f'更新: {a.speaker} → {alarm.speaker}')
                    new_alarm = False
                    break
            if new_alarm:
                alarm_list.append(alarm)

    # 列表按时间排序
    # alarm_list.reverse()
    return sorted(alarm_list, key=lambda a: a.dt)


if __name__ == '__main__':
    fn = '泛北防空识别区_20210826_152126_1010119710.txt'
    list = get_alarm_list(
        f'C:\\Users\\Hanse\\Documents\\EVE\\logs\\Chatlogs\\{fn}', 3600)

    print(len(list))
    for a in list:
        print(a)
