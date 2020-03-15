import requests
import js2py
import  execjs

context = js2py.EvalJs()

class BaiDuTranslater(object):
    ''''
        百度翻译爬虫
    '''
    def __init__(self,query):
        #初始化
        self.url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        self.query = query
        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36",
            'cookie': 'BAIDUID=5712A3D3904428F0E67B8DFE2A8F49C4:FG=1'
        }
        self.f = 'en'
        self.to = 'zh'

    def make_sign(self):
        #js逆向获取sign的值
        #读取js文件
        with open('translate.js','r',encoding='utf-8') as f:
            # context.execute(f.read())
            sign = execjs.compile(f.read()).call('e',self.query)
        #调用js中的函数生成sign
        # sign = context.a(self.query)
        #将sign加入到data中
        return sign

    def make_data(self,sign):
        # 判断输入的是英文还是中文
        if self.query.encode('utf-8').isalpha():
            self.f = 'en'
            self.to = 'zh'
        else:
            self.f = 'zh'
            self.to = 'en'
        data = {
            "query": self.query,
            "from": self.f,
            "to": self.to,
            "token": "846d18897e74bcf5d8e3f149fbee8cb9",
            "sign": sign
        }
        return  data

    def get_content(self,data):
        response = requests.post(url=self.url,headers=self.headers,data=data)
        # print(response.text)
        # print(response.status_code)
        return response.json()['trans_result']['data'][0]

    def run(self):
        '''运行程序'''
        #获取sign的值
        sign = self.make_sign()
        #构建参数
        data = self.make_data(sign)
        #获取翻译内容
        content = self.get_content(data)
        print(content['dst'])

if __name__ == '__main__':
    while True:
        query = input("请输入你要翻译的内容(输入EOF结束翻译)：")
        if query != 'EOF':
            translater = BaiDuTranslater(query)
            translater.run()
        else:
            break