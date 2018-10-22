import json
import requests
from urllib.parse import urlencode


def get_url_html(url, data, head):
    response = requests.post(url, data, headers=head)
    if response.status_code == 200:
        return response.text


def parse_html_json(html_text):
    json_dict = json.loads(html_text)
    job_info_list = json_dict["content"]["positionResult"]["result"]
    for job_info in job_info_list:
        positionName = job_info["positionName"]
        workYear = job_info["workYear"]
        education = job_info["education"]
        city = job_info["city"]
        positionAdvantage = job_info["positionAdvantage"]
        salary = job_info["salary"]
        companyLabelList = job_info["companyLabelList"]
        companyFullName = job_info["companyFullName"]
        print(positionName, salary, workYear, education, city, positionAdvantage, companyLabelList, companyFullName)


if __name__ == '__main__':
    keyword = input("Please enter the job you want: ")
    work_city = input("Please enter a work location: ")
    kw_data = {"kw": keyword}

    data = {
        "gj": "3年及以下",
        "px": "default",
        "city": work_city
    }

    head = {
        "Referer": "https://www.lagou.com/jobs/list_%s?" % urlencode(kw_data)[3:] + urlencode(data),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    for page in range(5):
        try:
            form_data = {
                "gj": "3年及以下",
                "px": "default",
                "city": work_city,
                "pn": page,
                "needAddtionalResult": "false"
            }

            url = "https://www.lagou.com/jobs/positionAjax.json?"

            html_text = get_url_html(url, form_data, head)
            parse_html_json(html_text)
        except:
            break
