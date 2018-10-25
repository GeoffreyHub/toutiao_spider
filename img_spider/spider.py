#!/usr/bin/env python
# encoding: utf-8

"""
@version: python37
@author: Geoffrey
@file: spider.py
@time: 18-10-24 上午11:15
"""
import json
import re
from multiprocessing import Pool
import urllib3
urllib3.disable_warnings()
from requests import RequestException

from common.request_help import make_session
from db.mysql_handle import MysqlHandler
from img_spider.settings import *



class SpiderTouTiao:


    def __init__(self, keyword):
        self.session = make_session(debug=True)
        self.url_index = 'https://www.toutiao.com/search_content/'
        self.keyword = keyword
        self.mysql_handler = MysqlHandler(MYSQL_CONFIG)

    def search_index(self, offset):
        url = self.url_index
        data = {
            'offset': offset,
            'format': 'json',
            'keyword': self.keyword,
            'autoload': 'true',
            'count': '20',
            'cur_tab': '3',
            'from': 'gallery'
        }

        try:
            response = self.session.get(url, params=data)
            if response.status_code is 200:
                json_data = response.json()
                with open(f'../json_data/搜索结果-{offset}.json', 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                return self.get_gallery_url(json_data)
        except RequestException:
            print('请求失败')

    @staticmethod
    def get_gallery_url(json_data):
        dict_data = json.dumps(json_data)
        for info in json_data["data"]:
            title = info["title"]
            gallery_pic_count = info["gallery_pic_count"]
            article_url = info["article_url"]
            yield title, gallery_pic_count, article_url

    def gallery_list(self, search_data):
        gallery_urls = {}
        for title, gallery_pic_count, article_url in search_data:
            print(title, gallery_pic_count, article_url)
            response = self.session.get(article_url)
            html = response.text
            images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
            result = re.search(images_pattern, html).group(1)

            if result:
                # result = result.replace('\\', '')
                # result = re.sub(r"\\", '', result)
                result = eval("'{}'".format(result))
                result = json.loads(result)
                # picu_urls = zip(result["sub_abstracts"], result["sub_titles"], [url["url"] for url in result["sub_images"]])
                picu_urls = zip(result["sub_abstracts"], [url["url"] for url in result["sub_images"]])
                # print(list(picu_urls))
                gallery_urls[title] = picu_urls
            else:
                print('解析不到图片ｕrl')

            with open(f'../json_data/{title}-搜索结果.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

            break

        # print(gallery_urls)
        return gallery_urls

    def get_imgs(self, gallery_urls):
        params = []
        for title, infos in (gallery_urls.items()):
            for index, info  in enumerate(infos):
                abstract, img_url = info
                print(index, abstract)
                response = self.session.get(img_url)
                img_content = response.content
                params.append([title, abstract, img_content])

                with open(f'/home/geoffrey/图片/今日头条/{title}-{index}.jpg', 'wb') as f:
                    f.write(img_content)

        print(f'正在保存' + '-'*50)
        SQL = 'insert into img_gallery(title, abstract, imgs) values(%s, %s, %s)'
        self.mysql_handler.insertMany(SQL, params)
        self.mysql_handler.end()


def main(offset):
    spider = SpiderTouTiao(KEY_WORD)
    search_data = spider.search_index(offset)
    gallery_urls = spider.gallery_list(search_data)
    spider.get_imgs(gallery_urls)


if __name__ == '__main__':
    groups = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]

    # pool = Pool()
    # pool.map(main, groups)

    for i in groups:
        main(i)


