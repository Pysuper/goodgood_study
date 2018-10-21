import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def url_get_html(url, data, head):
    """获取当前访问的页面源码"""
    from_data = urlencode(data)
    req = Request(url=url, data=from_data.encode("utf-8"), headers=head)
    response = urlopen(req).read().decode()
    return response


def parse_url_html(html_text):
    """处理请求回来的json字符串"""
    json_dict = json.loads(html_text)
    info_list = json_dict["data"]["mList"]
    for info in info_list:
        name = info["name"]
        price = info["price"]
        sellMode = info["sellMode"]
        yield name, price, sellMode


def save_com_info(name, price, sellMode):
    """保存从网页中获取的数据"""
    with open("./装备前线.text", "a", encoding="utf-8") as f:
        f.write(name + "    " + price + "   " + sellMode + "\n")
        print(name)


def main():
    url = "http://www.zfrontier.com/mchTagFilter"
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "X-CSRF-TOKEN": "1540102720b8f4dabceabfe22261717951ba5da0"
    }
    page = int(input("请输入访问的页数: "))
    data = {"tagIds[]": 140, "page": page - 1}

    # 从当前页面中获取想要的信息
    html_text = url_get_html(url, data, head)
    for name, price, sellMode in parse_url_html(html_text):
        save_com_info(name, price, sellMode)


if __name__ == '__main__':
    main()
