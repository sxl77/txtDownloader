import html
import os
import re
import time

import requests
from pyquery import PyQuery as pq


def get_web_contents(url, encoding):
    r = requests.get(url)
    r.encoding = encoding
    return r.text


def get_test_web_contents(url, encoding, selector):
    print(selector)
    r = requests.get(url)
    r.encoding = encoding
    if selector.strip() != '':
        result = pq(r.text)(selector)
    else:
        result = r.text
    return str(result)


def get_chapter_list(list_path, encoding, selector, chapter_url_prefix):
    r = requests.get(list_path)
    r.encoding = encoding
    charter_list = pq(r.text)(selector)
    down_url_dict = {}
    for item in charter_list.items():
        title = clear_title(item.html())
        # url_path = root_url + item.attr('href')
        if chapter_url_prefix == '':
            url_path = get_complete_url(list_path, item.attr('href'))
        else:
            url_path = chapter_url_prefix + item.attr('href')
        if title not in down_url_dict.keys():
            down_url_dict[title] = url_path
    return down_url_dict


def get_complete_url(list_url, txt_url):
    list_url_prefix = list_url[:list_url.rfind('/')]
    txt_url_prefix = txt_url[:txt_url.rfind('/')]
    complete_url = list_url_prefix.replace(txt_url_prefix, '') + '/' + txt_url
    return complete_url.replace('//', '/').replace(':/', '://')


def get_txt_content(url, encoding, selector):
    try:
        r = requests.get(url)
        r.encoding = encoding
        txt_content = pq(r.text)(selector).html()
        return clear_content(txt_content)
    except requests.ConnectionError:
        print('连接失败，重新连接。。。')
        time.sleep(1)
        return get_txt_content(url, encoding, selector)


def write_to_txt(txt_path, title, content):
    txt_path = txt_path.replace("/", '\\')
    txt_dir = txt_path[:txt_path.rfind('\\')] + '\\'
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    fp = open(txt_path, 'a', encoding="utf-8")
    fp.write('\n' + title + '\n' + content)
    fp.close()


def clear_content(content):
    content = content.replace("&nbsp", " ") \
        .replace("<br/>", "\n") \
        .replace("<br />", "\n") \
        .replace("<br>", "\n")
    content = re.sub('</?.+?/?>', '', content)
    content = re.sub('\\d{4}-\d{\1-\12}-\d{\1-\31}?', '', content)
    return html.unescape(content)


def clear_title(title):
    # title = re.sub('</?.+?/?>.+?</?.+?/?>|</?.+?/?>|[|?/:*]', '', title)
    title = re.sub('</?.+?/?>|[|?/:*]', '', title)
    title = title.replace('\t', '').replace('\n', '')
    title = html.unescape(title)
    return title


if __name__ == '__main__':
    # content = get_web_contents('http://www.haxixs.com/files/article/html/37/37810/index.html', 'gbk')
    # get_chapter_list(content, '.chapterlist a', '')
    # get_web_contents('https://www.runoob.com/python/python-gui-tkinter.html')
    print(get_txt_content('http://www.haxixs.com/files/article/html/70/70607/11035663.html', 'gbk', '#BookText'))
