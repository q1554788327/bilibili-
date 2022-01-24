import requests
import re
import json
import os
import datetime

#定义目录的全局变量
datetime_dir = datetime.datetime.today()
date_dir = datetime_dir.strftime("%Y-%m-%d")
time_dir = datetime_dir.strftime("%H-%M-%S")

#请求函数，返回网页的内容
def ask_url(url):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    #如果挂节点需要使用代理
    proxy = {
        "http":"http://127.0.0.1:7890",
        "https":"http://127.0.0.1:7890"
    }
    response = requests.get(url,timeout=3,proxies=proxy,headers=header)
    return response.text

#解析函数，返回需要转换的字典
def parse_data(url):
    works = []
    pattern = re.compile("window.__INITIAL_STATE__=(.*?);")
    response = ask_url(url)

    data = json.loads(re.findall(pattern,response)[0])["rankList"]
    for item in data:
        work = {
            "class":item["tname"],
            "title":item["title"],
            "cover":item["pic"],
            "author":item["owner"],
            "status":item["stat"]
        }
        works.append(work)
    return {datetime_dir.strftime("%Y-%m-%d %H:%M:%S"):works}

#保存数据的函数，将每个时刻的数据保存在json文本中
def save_data(works_dict):
    if os.path.exists("./data"):
        pass
    else:
        os.mkdir("./data")
    os.chdir("./data")
    if os.path.exists(date_dir):
        pass
    else:
        os.mkdir(date_dir)
    data_json = json.dumps(works_dict)
    os.chdir(date_dir)
    with open("{title}.json".format(title=time_dir),"w",encoding="utf-8") as f:
        f.write(data_json)

#主函数
def main():
    url = "https://www.bilibili.com/v/popular/rank/douga"
    works_dict = parse_data(url)
    #打印出数据字典
    print(works_dict)
    save_data(works_dict)

if __name__ == "__main__":
    main()

