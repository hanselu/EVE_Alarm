import json
from os.path import abspath, exists
from copy import deepcopy


class TYPE_NAME:
    Region: int = 1
    Constellation: int = 2
    SolarSystem: int = 3


region_list = []
constellation_list = []
solar_system_name_list = []

empire_area_name_list = [
    '卡多尔', '吉勒西斯', '塔什蒙贡', '幽暗之域', '柯埃佐', '破碎', '艾里迪亚',
    '伏尔戈', '暗涌之域', '赛塔德洱', '长征',
    '埃维希尔', '孤独之域''宁静之域', '精华之域', '维格温铎', '金纳泽',
    '摩登赫斯', '美特伯里斯', '西玛特尔',
    '德里克',
    '卡尼迪',
    '波赫文'
]

# 南北方星域待定
north_area_name_list = [
    '特纳', '血脉', '德克廉', '维纳尔', '斐德', '黑渊', '云环', '外环', '源泉之域',
    '辛迪加', '特布特', '静寂谷', '对舞之域', '钴蓝边域', '域外走廊', '欧莎',
    '佩利根弗', '糟粕之域', '卡勒瓦拉阔地', '琉蓝之穹', '螺旋之域'
]

# 南北方星域待定
south_area_name_list = [
    '绝地之域', '逑瑞斯', '贝斯', '普罗维登斯', '大荒野', '柯尔斯', '灼热之径',
    '邪恶湾流', '底特里德', '因斯姆尔', '地窖', '伊梅瑟亚', '特里菲斯', '卡彻',
    '混浊', '绝经', '埃索特亚', '摄魂之域', '非塔波利斯', '欧米斯特'
]

gm_area_name_list = ['A821-A', 'J7HZ-F', 'UUA-F4']

wormhole_name_list = [
    'K-R00033',
    'G-R00031',
    'A-R00001',
    'A-R00002',
    'A-R00003',
    'B-R00004',
    'B-R00005',
    'B-R00006',
    'B-R00007',
    'B-R00008',
    'C-R00009',
    'C-R00010',
    'C-R00011',
    'C-R00012',
    'C-R00013',
    'C-R00014',
    'C-R00015',
    'D-R00016',
    'D-R00017',
    'D-R00018',
    'D-R00019',
    'D-R00020',
    'D-R00021',
    'D-R00022',
    'D-R00023',
    'E-R00024',
    'E-R00025',
    'E-R00026',
    'E-R00027',
    'E-R00028',
    'E-R00029',
    'F-R00030',
    'H-R00032'
]

test_area_name_list = ['ADR01', 'ADR02', 'ADR03', 'ADR04', 'ADR05', 'PR-01']


def init_data():
    global region_list
    global constellation_list
    global solar_system_name_list

    # 读取数据
    def load_data_file(data_file: str) -> list:
        if exists(data_file):
            with open(data_file, 'r', encoding='utf8') as fp:
                return json.load(fp)

    # 初始化星域数据
    if region_list is None or len(region_list) == 0:
        # print('读取星域数据')
        region_list = load_data_file(abspath(r'.\data\region.json'))

    # 初始化星座数据
    if constellation_list is None or len(constellation_list) == 0:
        # print('读取星座数据')
        constellation_list = load_data_file(
            abspath(r'.\data\constellation.json'))

    # 初始化星系数据
    if solar_system_list is None or len(solar_system_list) == 0:
        # print('读取星系数据')
        solar_system_list = load_data_file(
            abspath(r'.\data\solar_system.json'))


def get_id_list(name_list: list, type_name: TYPE_NAME) -> list:
    """
    将名称列表转换为对应的ID列表
    """
    id_list = []
    if type_name == TYPE_NAME.Region:
        full_list = region_list
    elif type_name == TYPE_NAME.Constellation:
        full_list = constellation_list
    elif type_name == TYPE_NAME.SolarSystem:
        full_list = solar_system_name_list

    for item in full_list:
        if item['name'] in name_list:
            id_list.append(item['id'])

    return id_list


def get_region_id_list(name_list: list) -> list:
    """
    将星域名列表转换成星域ID列表
    """
    return get_id_list(name_list, TYPE_NAME.Region)


def get_constellation_id_list(name_list: list) -> list:
    """
    将星座名列表转换成星域ID列表
    """
    return get_id_list(name_list, TYPE_NAME.Constellation)


def get_solar_system_id_list(name_list: list) -> list:
    """
    将星系名列表转换成星域ID列表
    """
    return get_id_list(name_list, TYPE_NAME.SolarSystem)


def remove_filter_list(solar_list: list, filter_id_list: list, key: str) -> list:
    """
    移除筛选列表中的条目
    """
    new_list = deepcopy(solar_list)
    for s in solar_list:
        if s[key] in filter_id_list:
            new_list.remove(s)

    return new_list


def get_solar_system_list(all_universe: bool = True,
                          only_north: bool = False,
                          only_sourth: bool = False,
                          empire_area: bool = True,
                          white_list: dict = None,
                          black_list: dict = None,
                          wormhole: bool = False,
                          gm_area: bool = False,
                          test_area: bool = False
                          ) -> list:
    init_data()
    if all_universe:
        return solar_system_name_list

    watch_list = deepcopy(solar_system_name_list)

    # 筛选虫洞星域
    if not wormhole:
        watch_list = remove_filter_list(
            watch_list, get_region_id_list(wormhole_name_list), 'region')

    # 筛选GM星域
    if not gm_area:
        watch_list = remove_filter_list(
            watch_list, get_region_id_list(gm_area_name_list), 'region')

    # 筛选测试星域
    if not test_area:
        watch_list = remove_filter_list(
            watch_list, get_region_id_list(test_area_name_list), 'region')

    # 筛选帝国区星域
    if not empire_area:
        watch_list = remove_filter_list(
            watch_list, get_region_id_list(empire_area_name_list), 'region')

    # 筛选北方星域
    if only_north:
        north_area_id_list = get_region_id_list(north_area_name_list)
        watch_list = deepcopy(solar_system_name_list)
        for s in solar_system_name_list:
            if s['region'] not in north_area_id_list:
                watch_list.remove(s)

    # 筛选南方星域
    if only_sourth:
        sourth_area_id_list = get_region_id_list(south_area_name_list)
        watch_list = deepcopy(solar_system_name_list)
        for s in solar_system_name_list:
            if s['region'] not in sourth_area_id_list:
                watch_list.remove(s)

    # 黑名单
    if black_list:
        black_region_id_list = get_region_id_list(
            black_list.setdefault('regions', []))
        black_constellation_id_list = get_constellation_id_list(
            black_list.setdefault('constellation', []))
        black_solar_system_id_list = get_solar_system_id_list(
            black_list.setdefault('solar_system', []))

        watch_list = remove_filter_list(
            watch_list, black_region_id_list, 'region')
        watch_list = remove_filter_list(
            watch_list, black_constellation_id_list, 'constellation')
        watch_list = remove_filter_list(
            watch_list, black_solar_system_id_list, 'id')

    # 白名单
    if white_list:
        white_regions_id_list = get_region_id_list(
            white_list.setdefault('regions', []))
        white_constellation_id_list = get_constellation_id_list(
            white_list.setdefault('constellation', []))
        white_solar_system_id_list = get_solar_system_id_list(
            white_list.setdefault('solar_system', []))

        # 遍历星域
        for s in watch_list:
            if s['region'] in white_regions_id_list:
                white_solar_system_id_list.append(s['id'])

        # 遍历星座
        for s in watch_list:
            if s['constellation'] in white_constellation_id_list:
                white_solar_system_id_list.append(s['id'])

        # 去重
        white_solar_system_id_list = list(set(white_solar_system_id_list))

        # 将白名单ID列表重新映射成星系列表
        white_solar_system_list = []
        for solar_system_id in white_solar_system_id_list:
            for s in solar_system_name_list:
                if s['id'] == solar_system_id:
                    white_solar_system_list.append(s)
                    break

        # 将白名单添加到列表
        for solar_system in white_solar_system_list:
            if solar_system not in watch_list:
                watch_list.append(solar_system)

    return watch_list


if __name__ == '__main__':
    init_data()
    print(f'星域数量：{len(region_list)}')
    print(f'星座数量：{len(constellation_list)}')
    print(f'星系数量：{len(solar_system_name_list)}\n')

    black_list = {
        'solar_system': ['舍勒拉', '拉什希亚']
    }

    w_list = get_solar_system_list(all_universe=False,  black_list=black_list)
    print(f'筛选后 星系数量：{len(w_list)}')
