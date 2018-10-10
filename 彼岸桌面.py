import requests
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen
from multiprocessing.pool import Pool



def get_one_html(url, headers, proxy):
    """获取首页源码"""
    response = requests.get(url, headers, proxies=proxy)
    response.encoding = 'gbk'
    if response.status_code == 200:
        return response.text
    print("访问出错，请重新连接！")


def get_detail_src(text):
    """获取原网页中详情页的链接"""
    html = BeautifulSoup(text, 'lxml')
    soup_list = html.find('div', class_='list').find_all('li')
    for soup in soup_list:
        href = 'http://www.netbian.com' + soup.a['href']
        yield href


def parse_detail(detail_text):
    """进一步获取详情页源码"""
    html = BeautifulSoup(detail_text, 'lxml')
    soup = html.find('div', class_='pic-down').find('a')
    href = "http://www.netbian.com" + soup['href']
    return href


def parse_finally(finally_html):
    """最后处理高清图片的URL链接"""
    html = BeautifulSoup(finally_html, 'lxml')
    soup = html.find('td', align="left").a
    return soup['title'], soup['href']


def save_image(title, href):
    """保存图片"""
    content = urlopen(href)
    with open('./images1/%s.jpg' % title[:-2], 'wb') as f:
        f.write(content.read())
        print("%s----正在下载..." % title[:-2])


def get_url():
    """获取所有页面的链接"""
    for num in range(2, 200):
        yield 'http://www.netbian.com/meinv/index_%d.htm' % num


def more_text(url):
    head = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36"}
    proxy = {"http": "120.55.90.16:8088"}
    text = get_one_html(url, head, proxy)
    for src in get_detail_src(text):
        try:
            detail_text = get_one_html(src, head, proxy)
            next_detail_url = parse_detail(detail_text)
            finally_html = get_one_html(next_detail_url, head, proxy)
            image_title, image_href = parse_finally(finally_html)
            yield image_title, image_href
        except:
            continue


def main(detail_url):
    print(detail_url)
    for image_title, image_href in more_text(detail_url):
        threading.Thread(target=save_image, args=(image_title, image_href)).start()


if __name__ == '__main__':
    pool = Pool(10)
    for detail in get_url():
        pool.apply_async(main, args=(detail,))
    pool.close()
    pool.join()

