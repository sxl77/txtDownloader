import configparser
import os
from urllib import parse

cf = configparser.ConfigParser()


# 导出配置
def export(conf_path, list_path, list_encoding, list_selector, chapter_url_prefix, chapter_encoding, chapter_selector,
           is_merge, dst_path, txt_name):
    conf_path = conf_path.replace("/", '\\')
    conf_dir = conf_path[:conf_path.rfind('\\')] + '\\'
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
    cf['my_conf'] = {
        "list_path": parse.unquote(list_path),
        "list_encoding": list_encoding,
        "list_selector": list_selector,
        "chapter_url_prefix": parse.unquote(chapter_url_prefix),
        "chapter_encoding": chapter_encoding,
        "chapter_selector": chapter_selector,
        "is_merge": is_merge,
        "dst_path": dst_path,
        "txt_name": txt_name
    }
    with open(conf_path, "w+", encoding='utf-8') as f:
        cf.write(f)


def get_current_path():
    # return os.path.dirname(os.path.abspath(__file__))
    return os.getcwd()
