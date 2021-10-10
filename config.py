import json
from os.path import exists, abspath, expanduser
import os

config = None

# 默认配置文件
default_config = {
    'log_path': expanduser('~\Documents\EVE\logs\Chatlogs'),
    'channel': '泛北防空识别区',
    'listener': '万分荣幸',
    'overtime': 1800,
    'special_overtime': 900,
    'ignore_distance': 25,
    'watch_area': {
        'all_universe': False,
        'only_north': True,
        'only_south': False,
        'empire_area': False,
        'wormhole': False,
        'gm_area': False,
        'test_area': False,
        'white_list': {
            'regions': [],
            'constellations': [],
            'solar_system': []
        },
        'black_list': {
            'regions': [],
            'constellations': [],
            'solar_system': []
        }
    },
    'warning_level': {
        'level_a': {
            'distance': 5,
            'color': [255, 0, 0]
        },
        'level_b': {
            'distance': 10,
            'color': [255, 255, 0]
        },
        'level_c': {
            'distance': 15,
            'color': [0, 170, 255]
        }
    }
}


# 读取配置文件
def load_config(creat_new_file: bool = False) -> dict:
    # 检查配置文件是否存在
    setting_file_path = abspath(r'.\config.json')

    # 删除旧配置文件
    if creat_new_file and exists(setting_file_path):
        os.remove(setting_file_path)

    if not exists(setting_file_path):
        # 无配置文件，创建默认配置文件
        print('创建默认配置文件')
        with open(setting_file_path, 'w', encoding='utf8') as fp:
            json.dump(default_config, fp, ensure_ascii=False, indent=4)
        return default_config
    else:
        # 读取配置文件
        print('读取默认配置文件')
        with open(setting_file_path, 'r', encoding='utf8') as fp:
            setting = json.load(fp)

        # 检查配置文件
        if setting['log_path'].lower() in ['auto', '']:
            setting['log_path'] = expanduser('~\Documents\EVE\logs\Chatlogs'),

        return setting


# 获取配置
def get_config() -> dict:
    global config
    if config:
        return config
    else:
        config = load_config()
        return config


if __name__ == '__main__':
    setting = load_config()
    print(setting)
    print(setting['listerer'])
