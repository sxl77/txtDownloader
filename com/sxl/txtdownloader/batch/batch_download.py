import os

import threadpool

from com.sxl.txtdownloader import WebUtils

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
    'cookie': 'a2640_online=no; Hm_lvt_991eafca18a67072b895bf22da43b5b5=1625040121; '
              'Hm_lvt_218c5415283defda78e3896a29c4d86b=1625040121; a2640_threadlog=%2C16%2C; a2640_ck_info=%2F%09; '
              'a2640_winduser=BgEAUwRabAdWUgJRA1cABwZRAlsHA1QEXFRRAwdWBgcGB1ILVg4Iaw%3D%3D; '
              'a2640_appuser=AQsHVQBbMAIAAAAHV1xVUwACBVEABVAFAFEHUQUAUgxTU1RYUQQPbQ%3D%3D; a2640_ol_offset=354; '
              'a2640_readlog=%2C36599%2C64174%2C64171%2C; a2640_lastpos=other; '
              'a2640_lastvisit=102%091625040307%09%2Fdomainjs.php%3Fv%3D81%26nogo%3D; '
              'Hm_lpvt_991eafca18a67072b895bf22da43b5b5=1625040309; '
              'Hm_lpvt_218c5415283defda78e3896a29c4d86b=1625040309 '
}

download_conf = {
    'list_encoding': '',
    'list_selector': '.tal a',
    'chapter_url_prefix': '',
    'chapter_encoding': '',
    'chapter_selector': '#idstpc',
    'dst_path': r'E:\下载\caoliu'
}


def download_caoliu(list_path, no):
    # list_path = 'https://www.clc852.com/thread.php?fid=16&page=226'
    list_encoding = download_conf['list_encoding']
    list_selector = download_conf['list_selector']
    chapter_url_prefix = download_conf['chapter_url_prefix']

    chapter_encoding = download_conf['chapter_encoding']
    chapter_selector = download_conf['chapter_selector']

    txt_url_dict = WebUtils.get_chapter_list(list_path, list_encoding, list_selector, chapter_url_prefix, headers)
    # print(txt_url_dict)

    dst_path = download_conf['dst_path']
    for title, url in txt_url_dict.items():
        msg = '开始下载：' + title + '\n' + url
        print(msg)
        txt_path = dst_path + '\\' + no + '\\' + title + '.txt'
        if os.path.exists(txt_path):
            print('文件已存在，跳过下载')
            continue
        content = WebUtils.get_txt_content(url, chapter_encoding, chapter_selector, headers=None)
        if len(content.encode()) < 2000:
            print('长度过短，跳过下载')
            continue
        WebUtils.write_to_txt(txt_path, title, content)
    print(list_path + '\n下载完成！！！！！！')


if __name__ == '__main__':
    base_url = 'https://www.clc852.com/thread.php?fid=16&page=%d'

    # 创建线程池
    pool = threadpool.ThreadPool(230)
    # 创建需求列表
    func_var_list = []
    for i in range(1, 230):
        url = base_url % i
        no = str(i)
        func_var_list.append((None, {'list_path': url, 'no': no}))
    # 创建需求
    reqs = threadpool.makeRequests(download_caoliu, func_var_list)
    # 把需求添加到线程池
    [pool.putRequest(req) for req in reqs]
    # 阻塞等待
    pool.wait()
