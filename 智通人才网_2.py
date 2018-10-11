import re
import requests
from urllib.parse import urlencode


class ZhiTong():
    def get_url(self, num=10):
        data = {
            'keyword': '设计师',
            'keywordType': 0,
            'locationList': 14010000,
            'pageNo': 5
        }

        url_list = []
        for i in range(num):
            url = "http://www.job5156.com/s/result/ajax.json?" + urlencode(data)
            url_list.append(url)
        return url_list

    def parse(self, url_list):
        results = []
        for url in url_list:
            response = requests.get(url)
            html = response.text
            result = re.findall(r'.*?"posName":"(.*?)","refreshDat.*?'
                                r'cityName":"(.*?)","townName":"(.*?)","provName":"(.*?)".*?'
                                r'"taoLabelList":(.*?)],.*?'
                                r'"reqWorkYearStr":"(.*?)",".*?'
                                r'"educationDegreeStr":"(.*?)",".*?', html, re.S)
            results.append(result)

            for info in result:
                ti = info[0]
                tl = re.sub('<em>', '', ti)
                title = re.sub('</em>', '', tl)
                location = info[3] + info[1] + info[2]
                label = info[4][1:]
                biao = re.sub('"', '', label)
                qina = re.sub(',', '-', biao)
                work = info[5]
                educ = info[6]
                print(title, qina, educ, work, location)


def main(num):
    spider = ZhiTong()
    url_list = spider.get_url(num)
    spider.parse(url_list)


if __name__ == '__main__':
    main(10)

