import sqlite3
import requests
import json
import os

charInfoList = [
    {'id': 1010119710, 'name': '万分荣幸', 'line1': 11, 'line2': 10, 'line3': 10},
    {'id': 561781271, 'name': '市场经济国家', 'line1': 5, 'line2': 9, 'line3': 10},
    {'id': 348727097, 'name': 'Oo搬运工oO', 'line1': 5, 'line2': 9, 'line3': 5},
    {'id': 462934341, 'name': '欠我10块', 'line1': 10, 'line2': 10, 'line3': 10},
    {'id': 550567487, 'name': 'T小商贩T', 'line1': 5, 'line2': 10, 'line3': 5},
    {'id': 2112019056, 'name': '水电费交了吗', 'line1': 3, 'line2': 10, 'line3': 10},
    {'id': 90364450, 'name': '卡特利娜', 'line1': 10, 'line2': 10, 'line3': 10},
    {'id': 2112021805, 'name': '卫生费交了吗', 'line1': 4, 'line2': 5, 'line3': 10},
    {'id': 1030843520, 'name': 'GaryYan', 'line1': 10, 'line2': 10, 'line3': 10},
    {'id': 185821167, 'name': 'Rainny Lee', 'line1': 5, 'line2': 5, 'line3': 9},
    {'id': 2112110951, 'name': '安静的白学家', 'line1': 4, 'line2': 5, 'line3': 0},
    {'id': 351496273, 'name': '产业女王', 'line1': 10, 'line2': 10, 'line3': 9},
    {'id': 92638993, 'name': '加达里攻城狮', 'line1': 9, 'line2': 10, 'line3': 10},
    {'id': 2112168749, 'name': '平静的白学家', 'line1': 3, 'line2': 5, 'line3': 0},
    {'id': 989475549, 'name': '更深的藍', 'line1': 10, 'line2': 10, 'line3': 10},
    {'id': 2112280675, 'name': 'FX-991', 'line1': 5, 'line2': 5, 'line3': 10},
    {'id': 794117064, 'name': '竹语随风', 'line1': 3, 'line2': 1, 'line3': 0},
    {'id': 2112277535, 'name': '不烧机油的EA888', 'line1': 1, 'line2': 1, 'line3': 0}
]


def getItemName(id: int) -> str:
    """
    根据ID获得物品名称

    :param id: 物品ID
    :return: 物品名称
    """
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    sql = f'SELECT name FROM Item WHERE id = {id};'
    cursor.execute(sql)
    res = cursor.fetchone()

    if res is None:
        name = f'未知物品{id}'
    else:
        name = res[0]

    conn.close()
    return name


def getSystemID(systemName: str) -> int:
    """
    根据星系名获取星系的ID[精确查找]
    :param systemName: 星系名
    :return: 星系ID，若找不到，则返回0
    """
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()
        sql = f"SELECT * FROM SystemInfo WHERE systemName='{systemName}'"
        cursor.execute(sql)
        res = cursor.fetchone()

        if res is None:
            systemID = 0
        else:
            systemID = res[0]

        return systemID


def searchSystemID(systemName: str) -> list:
    """
    根据星系名获取星系的ID[模糊查找]
    :param systemName: 星系名
    :return: 星系ID，若找不到，则返回0
    """
    with sqlite3.connect(dbFile) as conn:
        cursor = conn.cursor()
        sql = f"SELECT * FROM SystemInfo WHERE systemName like '%{systemName}%'"
        cursor.execute(sql)
        res = cursor.fetchone()

        systemIDList = []
        if res is not None:
            for i in res:
                systemID = res[0]
                systemName = res[1]
                systemIDList.append({
                    'id': systemID,
                    'name': systemName
                })

        return systemIDList


def getStationName(stationID: int) -> str:
    """
    根据ID获得NPC空间站名称

    :param stationID: NPC空间站ID
    :return: NPC空间站名称
    """
    # 特殊空间站列表
    specialList = {
        60003760: '海4',
        1013918880239: '星城'
    }

    if stationID in specialList:
        return specialList[stationID]
    else:
        # return '其他'

        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()
        sql = f'SELECT name FROM Station WHERE id = {stationID};'
        cursor.execute(sql)
        res = cursor.fetchone()

        if res is None:
            name = f'未知空间站{stationID}'
        else:
            name = res[0]

        conn.close()
        return name


def getItemInfo(id: int) -> dict:
    """
    根据ID获得物品信息

    :param id: 物品ID
    :return: 物品信息
    """
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    sql = f'SELECT * FROM Item WHERE id = {id};'
    cursor.execute(sql)
    res = cursor.fetchone()
    if res is None:
        name = f'未知物品{id}'
        type = []
    else:
        name = res[1]
        type = [res[2], res[3], res[4], res[5], res[6], res[7]]

    conn.close()
    return {
        'id': id,
        'name': name,
        'type': type
    }


def getItemTypeName(itemID: int) -> str:
    """
    获取物品的最小类型名

    :param itemID: 物品ID
    :return: 物品的最小类型名
    """
    info = getItemInfo(itemID)
    typeName = ''
    if len(info['type']) > 0:
        for tn in info['type']:
            if tn is not None:
                typeName = tn

    return typeName


def getItemID(name: str) -> int:
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    sql = f"SELECT * FROM Item WHERE name = '{name}';"
    cursor.execute(sql)
    res = cursor.fetchone()

    if res is None:
        id = -1
    else:
        id = res[0]

    conn.close()
    return id


def downloadPic(itemID: int, imgPath: str) -> bool:
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
        "Connection": "close",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
    }  # 伪装成浏览器

    imgURL = f'https://image.evepc.163.com/Type/{itemID}_64.png'

    res = requests.get(imgURL, headers=send_headers)
    if res.status_code == 200:
        with open(imgPath, 'wb') as code:
            code.write(res.content)
            itemName = getItemName(itemID)
            print(f'下载 {itemID} {itemName}')
        return True
    else:
        return False


def getItemPicPath(id: int) -> str:
    path = f'./dat/icons/{id}_64.png'
    if not os.path.exists(path):
        downloadPic(id, path)
    return f'./dat/icons/{id}_64.png'


def getItemPicURL(id: int) -> str:
    return f'https://image.evepc.163.com/Type/{id}_64.png'


def getItemNameByServer(id: int) -> str:
    url = f'https://esi.evepc.163.com/latest/universe/types/{id}/?datasource=serenity&language=zh'
    res = requests.get(url)
    if res.status_code == 200:
        jsonObj = json.loads(res.text)
        return jsonObj['name']
    else:
        return f'未知物品{id}'


def searchItemID(name: str) -> int:
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    sql = f"SELECT id FROM Item WHERE name LIKE '%{name}%';"
    cursor.execute(sql)
    res = cursor.fetchall()

    if res is None:
        idList = []
    else:
        idList = []
        for i in res:
            idList.append(i[0])

    conn.close()
    return idList


def getCharName(charID: int) -> str:
    """
    根据ID获取角色名

    :param charID: 角色的ID
    :return: 角色的名称
    """
    for c in charInfoList:
        if c['id'] == charID:
            return c['name']

    return f'人物{charID}'


def getAllItems():
    """
    获得所有商品列表

    :return:所有商品的信息列表
    """
    conn = sqlite3.connect(dbFile)
    cursor = conn.cursor()
    sql = "SELECT * FROM Item WHERE type1 <> '' and id < 30"
    cursor.execute(sql)
    res = cursor.fetchall()

    if res is None:
        itemList = []
    else:
        itemList = []
        for i in res:
            id = i[0]
            name = i[1]
            type1 = i[2]
            type2 = i[3]
            type3 = i[4]
            type4 = i[5]
            type5 = i[6]
            type6 = i[7]
            itemList.append({
                'id': id,
                'name': name,
                'type1': type1,
                'type2': type2,
                'type3': type3,
                'type4': type4,
                'type5': type5,
                'type6': type6
            })

    conn.close()
    return itemList


if __name__ == '__main__':
    dbFile = 'eve.db'
else:
    # dbFile = './EVE/eve.db'
    dbFile = 'eve.db'
