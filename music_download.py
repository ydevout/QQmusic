import re
import random
import requests
import json
import time
import csv
import urllib
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
song_ids = []
song_names = []


def parse_page():
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.js_song')
    for s in info:
        song_id = str(re.findall('href="(.*?)"', str(s))).split('/')[6].split('\'')[0].split('.html')[0]
        song_ids.append(song_id)
    for s in info:
        song_name = str(re.findall('title="(.*?)"', str(s))).split('\'')[1]
        song_names.append(song_name)
    save_songs()
    # print(song_names)


def save_songs():
    for mid, name in zip(song_ids, song_names):
        size_c = 'C400' + mid + '.m4a'
        size_m = 'M800' + mid + '.mp3'  # 320KB下载格式
        guid = int(random.random() * 2147483647) * int(time.time() * 1000) % 10000000000
        d = {
            'format': 'json',
            'cid': 205361747,
            'uin': 0,
            'songmid': mid,
            'filename': size_c,
            'guid': guid,
            }
        proxies = ['60.216.101.46:59351', '42.202.130.246:3128', '122.228.25.97:8101', ]
        headers = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
            'Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 '
            'Safari/537.14',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
            'Safari/537.36'
        ]
        header = {'User-Agent': random.choice(headers)}
        print(size_c)
        print(size_m)
        print(header)
        try:
            r = requests.get('https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg', params=d,
                             headers=header)  # r.json()可以看到user_ip
            vkey = json.loads(r.content)['data']['items'][0]['vkey']
            song_url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=64' % (size_m, vkey, guid)
            path = 'D:\\song\\' + str(name) + '.mp3'
            try:
                urllib.request.urlretrieve(song_url, path),
                print('歌曲: %s 下载完成！' % name)
            except ConnectionError:
                print('歌曲: %s 下载失败！' % name)
                try:
                    print('更换文件大小重新下载中……')
                    new_name = 'M500' + mid + '.mp3'
                    new_url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s&uin=0&fromtag=64' % (new_name,
                                                                                                           vkey, guid)
                    path = 'D:\\song\\' + str(name) + '.mp3'
                    urllib.request.urlretrieve(new_url, path),
                    print('重新下载已完成！')
                except ConnectionError:
                    print('歌曲: %s 重新下载失败！' % name)
                    print('开始保存歌曲下载失败名单……')
                    data = {'歌曲名': name, '歌曲mid': mid}
                    with open('D:\\song\\failed.csv', 'a', newline='', encoding='utf-8') as f:
                        fieldnames = ['歌曲名', '歌曲mid']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerow(data)
                        print('名单保存成功！')
            time.sleep(2)
        except ConnectionError:
            print('request error')


if __name__ == '__main__':
    # singer = str(input("请输入歌手名："))
    singer = "于文文"
    for page in range(1, 2):
        url = 'https://y.qq.com/portal/search.html#page={page}&t=song&w={singer}'.format(page=page, singer=singer)
        parse_page()
