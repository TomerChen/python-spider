import json
from multiprocessing import Pool
import requests
import re
from requests.exceptions import  RequestException
import xlwt


def get_one_page(url):
    try:
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return  None
    except RequestException:
        return None

def parse_one_page(html):
    print("开始获取数据")
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip(),
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def write_to_excel(html,worksheet):
    for item in parse_one_page(html):
        print(item)
        global count
        worksheet.write(count,0,item.get('index'))
        worksheet.write(count,1,item.get('score'))
        worksheet.write(count,2,item.get('title'))
        worksheet.write(count,3,item.get('actor'))
        worksheet.write(count,4,item.get('time'))
        worksheet.write(count,5,item.get('image'))
        count=count+1

def main(offset,worksheet):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    write_to_excel(html,worksheet)
    # print(html)
    # for item in parse_one_page(html):
    #     print(item)
    #     write_to_file(item)



if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('猫眼电影Top100')
    count = 1
    # 设置单元格的宽度
    worksheet.col(2).width = 256 * 20
    worksheet.col(3).width = 550 * 20
    worksheet.col(4).width = 350 * 20

    worksheet.write(0, 0, '排名')
    worksheet.write(0, 1, '评分')
    worksheet.write(0, 2, '电影名称')
    worksheet.write(0, 3, '主演')
    worksheet.write(0, 4, '上映时间')
    worksheet.write(0, 5, '封面图片')
    for i in range(10):
        main(i*10,worksheet)
    workbook.save('猫眼电影Top100.xls')
    # 使用多进程爬取
    # pool = Pool()
    # pool.map(main,[i*10 for i in range(10)])
