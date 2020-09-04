import configparser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
default_config_file = os.path.join(BASE_DIR, 'configure.ini')


def get_configure(section, option, default='', config_file=default_config_file):
    # 获取配置文件中的配置
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return config.get(section, option)
    except:
        return default
