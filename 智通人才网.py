import json
import requests
from urllib.parse import urlencode
from fake_useragent import UserAgent


def get_url(key_word):
    """
    通过传入的关键字, 拿到该职位的网页链接
    :param key_word:
    :return:
    """
    for page in range(1, 10):
        data = {
            "keyword": key_word,
            "pageNo": page,
            }
        url = "http://www.job5156.com/s/result/ajax.json?" + urlencode(data).replace('+', '')
        print(url)
        yield url


def get_page_info(url):
    """
    通过当前访问的url链接, 获取网页源码
    :param url: 当前访问的页面链接
    :return: 当前页面的源码
    """
    head = {"User-Agent": "%s" % UserAgent().chrome}
    proxy = {'https': '106.75.226.36:808'}
    response = requests.get(url, headers=head, proxies=proxy)
    if response.status_code == 200:
        return response.text


def parse_json_info(json_text):
    """
    通过当前访问的页面的源码, 拿到里面的招聘信息, 并保存
    :param json_text: 当全部访问的网页源码
    :return: 数据保存的情况
    """
    info_dict = json.loads(json_text)
    for info in info_dict["page"]["items"]:
        title = info["posName"].replace('<em>', '').replace('</em>', '')
        
        content_dict = {
            "title": info["posName"].replace('<em>', '').replace('</em>', ''),
            "money": info["salaryStr"],
            "company_name": info["comName"],
            "label_list": info["taoLabelList"],
            "industry_str": info["industryStr"],
            "refresh_date": info["refreshDateStr"],
            "req_work_year": info["reqWorkYearStr"],
            "work_locations": info["workLocationsStr"]
        }

        content_json = json.dumps(content_dict, ensure_ascii=False)
        with open("zhi_tong.text", 'a', encoding="utf-8") as f:
            f.write(content_json)
            f.write('\n')
            print(title)


def main(key_word):
    """入口"""
    for url in get_url(key_word):
        json_text = get_page_info(url)
        if json.loads(json_text)["page"] == None:
            print("所有信息展示完毕...")
            break
        else:
            parse_json_info(json_text)


if __name__ == '__main__':
    key_word = input("请输入搜索的职位: ")
    main(key_word)

    
