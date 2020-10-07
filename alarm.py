import requests
import re
import time
import json
import EVE_DB
import os
import ctypes
from ctypes.wintypes import MAX_PATH

baseSystemName = 'ZK-YQ3'
baseSystemID = 0
overtime = 300
alarmDistance = 10


def alarm_Init():
    global baseSystemID
    baseSystemID = EVE_DB.getSystemID(baseSystemName)


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


def analysisLog(logStr: str) -> dict:
    """
    解析日志内容
    :param logStr: 日志原文
    :return:
    """
    # match = re.match(r'\[ (?P<Time>\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) ] (?P<Char>.*) > (?P<Content>.*)'
    #                  , logStr)
    match = re.search(
        r'\[ (?P<Time>\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2}) ] (?P<Char>.*) > .*(?P<SystemName>([a-zA-Z]|\d)+-([a-zA-Z]|\d)+)'
        , logStr)
    if match is not None:
        timeStr = match.group('Time')
        ts = int(time.mktime(time.strptime(timeStr, '%Y.%m.%d %H:%M:%S')))
        charName = match.group('Char')
        systemName = match.group('SystemName')
        return {
            'ts': ts,
            'char': charName,
            'systemName': systemName
        }
    else:
        return {}


def calRoute(targetSystemID: int) -> int:
    if targetSystemID == baseSystemID:
        return 0

    url = f'https://esi.evepc.163.com/latest/route/{baseSystemID}/{targetSystemID}/?datasource=serenity&flag=shortest'
    ret = requests.get(url)
    if ret.status_code == 200:
        return len(json.loads(ret.text)) - 1
    else:
        return -1


def calDistance(targetSystemName: str) -> int:
    targetSystemList = EVE_DB.searchSystemID(targetSystemName)
    distanceList = []
    for s in targetSystemList:
        distanceList.append(calRoute(s['id']))

    return min(distanceList)


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


def getAlarmList(logFilePath: str) -> list:
    with open(logFilePath, 'r', encoding='utf16') as f:
        logList = re.findall(r'\[ \d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2} ] .* > .*', f.read())
        alarmList = []
        for log in logList:
            logInfo = analysisLog(log)
            if logInfo == {}:
                continue

            dt = int(time.time()) - logInfo['ts']
            if dt <= overtime:
                # logInfo['dic'] = calDistance()
                logInfo['dt'] = showTimeDiff(dt)
                distance = calDistance(logInfo['systemName'])
                logInfo['distance'] = distance
                alarmList.append(logInfo)

        print('长度', len(alarmList))
        return alarmList


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


alarm_Init()
logFileName = getLogPath('泛北防空识别区', '欠我10块')
print(logFileName)
for alarim in getAlarmList(logFileName):
    print(alarim)

# print(calDistance('罗尔'))

# print(EVE_DB.searchSystemID('zk'))
