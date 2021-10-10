import requests
import json
from os.path import exists
from os import makedirs

solar_system_dict = {}
solar_system_list = []


def init():
    global solar_system_dict
    with open('./data/solar_system.json', 'r', encoding='utf8') as f:
        solar_system_dict = json.load(f)


def get_solar_system_id(solar_system_name: str) -> int:
    if len(solar_system_dict) == 0:
        init()

    for solar_system in solar_system_dict:
        if solar_system['name'] == solar_system_name:
            return solar_system['id']

    print(f'无此星系: {solar_system_name}')
    return None


def get_solar_system_name(solar_system_id: int) -> str:
    if len(solar_system_dict) == 0:
        init()

    for solar_system in solar_system_dict:
        if solar_system['id'] == solar_system_id:
            return solar_system['name']

    return f'未知星系{solar_system_id}'


def get_solar_system_name_list() -> list:
    global solar_system_list

    if len(solar_system_list) == 0:
        init()

    name_list = []
    for solar_system in solar_system_dict:
        name_list.append(solar_system['name'])

    return name_list


def _get_character_id_from_esi(character_name: str) -> int:
    """
    从ESI获取角色ID
    """

    url = 'https://esi.evepc.163.com/latest/universe/ids/?datasource=serenity&language=zh'
    data = json.dumps([character_name])
    response = requests.post(url, data)
    if response.status_code == 200:
        info = json.loads(response.text)
        if 'characters' in info:
            return info['characters'][0]['id']

    print(f'获取角色【{character_name}】ID失败: {response.status_code}')
    return None


def get_character_id(character_name: str) -> int:
    """
    从缓存获取角色ID
    """

    # 判断缓存文件夹是否存在
    if not exists('cache'):
        print('创建缓存文件夹')
        makedirs('cache')

    # 判断缓存文件是否存在
    cache_file_name = 'cache/id.json'
    if not exists(cache_file_name):
        id = _get_character_id_from_esi(character_name)

        if id:
            # 写入缓存
            with open(cache_file_name, 'w', encoding='utf8') as f:
                json.dump({character_name: id}, f, ensure_ascii=False)
            return id
    else:
        with open(cache_file_name, 'r', encoding='utf8') as f:
            id_dict = json.load(f)

        if character_name in id_dict:
            # print('命中缓存')
            return id_dict[character_name]
        else:
            id = _get_character_id_from_esi(character_name)
            id_dict[character_name] = id
            # 写入缓存
            with open(cache_file_name, 'w', encoding='utf8') as f:
                json.dump(id_dict, f, ensure_ascii=False)
            return id

    return None


def _get_route_from_esi(origin_id: int, destination_id: int) -> list:
    """
    从ESI获取星系距离
    """

    url = f'https://esi.evepc.163.com/latest/route/{origin_id}/{destination_id}/?datasource=serenity&flag=shortest'
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print('获取路径出错')
        return None


def cal_route(origin: str, destination: str) -> list:
    """
    获取星系距离
    """

    if origin == destination:
        return []

    # 获取星系ID
    origin_id = get_solar_system_id(origin)
    destination_id = get_solar_system_id(destination)

    if not origin_id:
        print(f'无此星系 {origin}')
        return None

    if not destination_id:
        print(f'无此星系 {destination}')
        return None

    # 判断缓存文件夹是否存在
    if not exists('cache'):
        print('创建缓存文件夹')
        makedirs('cache')

    # 判断缓存文件是否存在
    cache_file_name = f'cache/{origin}.json'
    if not exists(cache_file_name):
        route = _get_route_from_esi(origin_id, destination_id)

        if route:
            # 写入缓存
            with open(cache_file_name, 'w', encoding='utf8') as f:
                json.dump({destination: route}, f, ensure_ascii=False)
            return route
    else:
        with open(cache_file_name, 'r', encoding='utf8') as f:
            route_dict = json.load(f)

        if destination in route_dict:
            # print('命中缓存')
            return route_dict[destination]
        else:
            route = _get_route_from_esi(origin_id, destination_id)
            route_dict[destination] = route
            # 写入缓存
            with open(cache_file_name, 'w', encoding='utf8') as f:
                json.dump(route_dict, f, ensure_ascii=False)
            return route

    return None


def cal_distance(origin: str, destination: str) -> int:
    route = cal_route(origin, destination)
    if route:
        return len(route)
    else:
        return None


if __name__ == '__main__':
    # print(_get_distance_from_esi(30003658, 30003645))
    print(cal_route('ZK-YQ3', 'MZPH-W'))
    print(get_solar_system_name(33000041))
    print(get_solar_system_id('ZK-YQ3'))
