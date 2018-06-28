import os
import json

def get_mysql_schema_config(
    default_path='./../../data/mysql.json',
    env_key='MYSQL_CFG'
):
    """
    a
    :param default_path:
    :return:
    """
    path = default_path
    value = os.getenv(env_key, None)
    mysql = []
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            mysql = json.load(f)
    return mysql
