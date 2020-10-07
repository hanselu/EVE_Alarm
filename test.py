import ctypes
import json
import os
import re
import time
from ctypes.wintypes import MAX_PATH

import EVE_DB
import requests

# logFileName = r'C:\Users\Hanse\Documents\EVE\logs\Chatlogs\泛北防空识别区_20201006_051238.txt'
logFileName = ''
baseSystemName = '3-QYVE'
baseSystemID = 0
passTime = 900


def alarm_Init():
    global baseSystemID
    global logFileName
    baseSystemID = EVE_DB.getSystemID(baseSystemName)
    logFileName = getLogPath('泛北防空识别区', '欠我10块')


def getFirstRe(reStr: str, searchStr: str) -> str:
    """
    获取正则表达式的第一个匹配值
    :param reStr: 正则表达式
    :param searchStr: 要搜索的字符串
    :return: 第一个匹配的结果，若无匹配则返回空字符串
    """
    match = re.search(reStr, searchStr)
    if match is not None:
        return match.group(0)
    else:
        return ''


def getLogListener(logFilePath: str) -> str:
    """
    读取日志文件的监听者。
    :param logFilePath:  日志文件路径
    :return: 监听者名字，若无则返回空字符串。
    """
    listener = ''
    with open(logFilePath, 'r', encoding='utf16') as f:
        for line in f:
            m = re.match(r'^\s+Listener:\s+(.*)$', line)
            if m is not None:
                # print(line)
                listener = m.group(1)
                break

    return listener


def getLogPath(channelName: str = '', listener: str = '') -> list:
    """
    获取日志路径
    :param channelName: 指定频道名字
    :param listener:  指定人物
    :return:  日志文件路径
    """
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        logDir = f'{buf.value}\\EVE\\logs\\Chatlogs\\'
        files = []
        for (dirPath, dirNames, fileNames) in os.walk(logDir):
            for fn in fileNames:
                # 把 dirpath 和 每个文件名拼接起来 就是全路径
                # print(fn)
                ts = int(time.mktime(time.strptime(getFirstRe(r'(?<=_)\d{8}_\d{6}(?=.txt)', fn), '%Y%m%d_%H%M%S')))
                ts += 8 * 3600  # 修正时区
                # print(ts)
                # print(getFirstRe(r'(?<=_)\d{8}_\d{6}(?=.txt)', fn))
                fPath = os.path.join(dirPath, fn)

                files.append({
                    'name': fPath,
                    'ts': ts
                })

        # 排序文件
        files.sort(key=lambda f: -f['ts'])

        for logFile in files:
            if channelName in logFile['name']:
                if listener in getLogListener(logFile['name']):
                    return logFile['name']

        return ''


def getLogText():
    with open(logFileName, 'r', encoding='utf16') as f:
        return f.read()


def getTimestamp(logStr: str) -> int:
    m = re.search(r'\[ (\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) ]', logStr)
    if m is None:
        return -1

    timeStr = m.group(0)
    return int(time.mktime(time.strptime(timeStr, '[ %Y.%m.%d %H:%M:%S ]')))


def getChar(logStr: str) -> str:
    m = re.search(r'\[ \d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2} ] (.*) >', logStr)
    if m is None:
        return ''

    return m.group(1)


def getSystemName(logStr: str) -> str:
    m = re.findall(r'[a-zA-Z0-9]+-[a-zA-Z0-9]+', logStr)
    if m is None:
        return ''

    return m[0]


def calRoute(targetSystemID: int) -> int:
    if targetSystemID == baseSystemID:
        return 0

    url = f'https://esi.evepc.163.com/latest/route/{baseSystemID}/{targetSystemID}/?datasource=serenity&flag=shortest'
    ret = requests.get(url)
    if ret.status_code == 200:
        return len(json.loads(ret.text)) - 1
    else:
        return -1


def showTimeDiff(dt: int) -> str:
    h = int(dt / 3600)
    m = int((dt - h * 3600) / 60)
    s = dt - h * 3600 - m * 60

    dtStr = ''

    if h > 0:
        dtStr = f'{h}小时'

    if m > 0:
        dtStr = f'{dtStr}{m}分'

    return f'{dtStr}{s}秒前'


def updateAlarmList(aList: list, al: dict) -> list:
    isNewAlarm = True
    for a in aList:
        if a['name'] == al['name']:
            if al['dt'] < a['dt']:
                a['dt'] = al['dt']
                a['time'] = a['time']
                isNewAlarm = False
                break
            break

    if isNewAlarm:
        aList.append(al)

    return aList


def getAlarmIndex(aList: list, al: dict) -> int:
    for index, a in enumerate(aList):
        if a['name'] == al['name']:
            if al['dt'] < a['dt']:
                a['dt'] = al['dt']
                a['time'] = a['time']
                return index
            else:
                return -2

    return -1


def getAlarmList() -> list:
    global passTime
    allLines = re.findall(
        r'\[ \d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2} ] .* > .*[a-zA-Z0-9]{1,4}-[a-zA-Z0-9]{1,4}.*', getLogText())

    alarmList = []
    for s in allLines:
        dt = int(time.time()) - getTimestamp(s)
        if dt < passTime:
            name = getSystemName(s)
            systemID = EVE_DB.getSystemID(name)
            if systemID == 0:
                continue

            # distance = calRoute(systemID)
            alarm = {
                'dt': dt,
                'time': showTimeDiff(dt),
                'char': getChar(s),
                'name': name,
                # 'distance': distance
            }
            index = getAlarmIndex(alarmList, alarm)
            if index >= 0:
                alarmList[index]['dt'] = alarm['dt']
                alarmList[index]['time'] = alarm['time']
                alarmList[index]['char'] = alarm['char']
            elif index == -1:
                alarm['distance'] = calRoute(systemID)
                alarmList.append(alarm)

            # updateAlarmList(alarmList, alarm)
            # alarmList.append(alarm)
            # print(alarm)
    alarmList.sort(key=lambda a: a['dt'])
    return alarmList


if __name__ == '__main__':
    alarm_Init()
    getAlarmList()
