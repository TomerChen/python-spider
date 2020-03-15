import time

from selenium import webdriver

class DouYu:
    def __init__(self):
        self.start_url = 'https://www.douyu.com/g_LOL'
        self.driver = webdriver.Chrome()
        self.i = 0
        pass

    def get_content_list(self):
        self.i=self.i+1
        li_list = self.driver.find_elements_by_xpath('//ul[@class="layout-Cover-list"]/li')
        page_num = self.driver.find_element_by_xpath('//*[@id="listAll"]/div[2]/div/ul/li[@class="dy-Pagination-item dy-Pagination-item-{} dy-Pagination-item-active"]/a'.format(self.i)).text
        content_list = []
        print("正在抓取第{}页数据".format(int(page_num)))
        for li in li_list:
            item = {}
            item_div = li.find_element_by_xpath('.//div[@class="DyListCover-content"]')
            item['type'] = item_div.find_element_by_xpath('./div[@class="DyListCover-info"]/span').text
            item['title'] = item_div.find_element_by_xpath('./div[@class="DyListCover-info"]/h3').text
            item['anchor'] = item_div.find_element_by_xpath('./div[@class="DyListCover-info"]/h2').text
            item['hot'] = item_div.find_element_by_xpath('./div[@class="DyListCover-info"]/span[@class="DyListCover-hot"]').text
            try:
                item['headerCell'] = item_div.find_element_by_xpath('./span[@class="HeaderCell-label-wrap is-od"]').text
            except:
                item['headerCell'] = '无'
            print(item)
            time.sleep(0.01)
            content_list.append(item)
        next_button = self.driver.find_elements_by_xpath('//*[@id="listAll"]/div[2]/div/ul/li[9]/span')
        next_button = next_button[0] if len(next_button)>0 else None
        return content_list,next_button

    def save_content_list(self,content_list):
        with open("douyu.txt",'a',encoding='utf-8') as f:   #'a'为追加写入，'w'为覆盖写入，'r'为只读
            f.write("\n".join("{}".format(i) for i in content_list))
        pass

    def run(self):
        #1.发送请求，访问斗鱼英雄联盟板块
        self.driver.get(self.start_url)
        self.driver.maximize_window()
        #2.提取数据
        content_list,next_btn = self.get_content_list()
        #3.保存数据
        self.save_content_list(content_list)
        #4.提取下一页数据
        for i  in range(3):
            if next_btn is not None:
                next_btn.click()
                time.sleep(2)
                content_list,next_btn = self.get_content_list()
                self.save_content_list(content_list)
        #5.关闭浏览器
        self.driver.close()
        pass

if __name__ == '__main__':
    douyu = DouYu()
    douyu.run()
    pass