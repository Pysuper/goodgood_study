import re
import pymysql
import requests
import six.moves
import urllib.parse
from lxml import etree
from urllib.parse import urlencode


def parse_detail_url(page_url):
    """
    通过当前页的链接--获取到该页面的招聘信息
    :param page_url: 页面的访问,链接
    :return: 各个信息的列表
    """
    work_name_list = []
    com_name_list = []
    work_place_list = []
    work_money_list = []
    print_day_list = []

    response = requests.get(page_url)
    response.encoding = "gbk"
    html = etree.HTML(response.text)
    print(page_url)

    title_list = html.xpath('//*[@id="resultList"]/div/p/span/a/text()')[1:]
    comply_list = html.xpath('//*[@id="resultList"]/div/span[1]/a/@title')[1:]
    place_list = html.xpath('//*[@id="resultList"]/div/span[2]/text()')[1:]
    money_list = html.xpath('//*[@id="resultList"]/div/span[3]')[1:]
    day_list = html.xpath('//*[@id="resultList"]/div/span[4]/text()')[1:]

    for i in money_list:
        if i.text != None:
            work_money_list.append(i.text)
        else:
            work_money_list.append("暂无")

    for title, comply, place, money, day in six.moves.zip(title_list, comply_list, place_list, money_list, day_list):
        work_name = re.sub('\W', '', title)
        com_name = re.sub('\W', '', comply)
        work_place = re.sub('\W', '', place)
        print_day = re.sub('\W', '', day)
        work_name_list.append(work_name)
        com_name_list.append(com_name)
        work_place_list.append(work_place)
        print_day_list.append(print_day)
    return work_name_list, com_name_list, work_place_list, work_money_list, print_day_list


def save_info(work_name_list, com_name_list, work_place_list, work_money_list, print_day_list):
    """将数据保存到数据库中"""
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           database='51job_test',
                           charset='utf8')

    # 获取游标
    cursor = conn.cursor()

    for work_name, com_name, work_place, work_money, print_day in six.moves.zip(work_name_list, com_name_list, work_place_list, work_money_list, print_day_list):
        day = print_day[:1] + "-" + print_day[2:]
        print(day)
        sql = "insert into 51_python(name,company,place,money,day) values('%s','%s','%s','%s','%s');" % (
            work_name, com_name, work_place, work_money, day)
        # sql = "insert into test(name,company,place,money,day) values(%s,%s,%s,%s,%s)" % (work_name, com_name, work_place, work_money, day)
        print(sql)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()


def main():
    """入口"""
    href_data = {
        "lang": " c",
        "stype": " 1",
        "postchannel": " 0000",
        "workyear": " 99",
        "cotype": " 99",
        "degreefrom": " 99",
        "jobterm": " 99",
        "companysize": " 99",
        "lonlat": " 0,0",
        "radius": " -1",
        "ord_field": " 0",
        "confirmdate": " 9",
        "fromType": " ",
        "dibiaoid": " 0",
        "address": " ",
        "line": " ",
        "specialarea": " 00",
        "from": " ",
        "welfare": " "
    }
    key_word = "Python工程师"
    k = re.sub('%', '%25', urllib.parse.quote(key_word))
    key = "Python%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588"
    
    # 拼接出完整的 URL
    href = "https://search.51job.com/list/020000,000000,0000,00,9,99," + key + ',2,'
    for i in range(1, 7):
        page = "%s.html?" % i
        url = href + page + urlencode(href_data)

        work_name_list, com_name_list, work_place_list, work_money_list, print_day_list = parse_detail_url(url)
        save_info(work_name_list, com_name_list, work_place_list, work_money_list, print_day_list)


if __name__ == '__main__':
    main()


   
