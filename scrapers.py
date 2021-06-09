from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

# Eztravel用
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
my_options = Options()
my_options.add_argument("--headless")
driver = webdriver.Chrome(options=my_options)# 不開啟實體瀏覽器


# 票券網站抽象類別
class Website(ABC):
    def __init__(self, city_name, lower_limit, upper_limit):
        self.city_name = city_name # 城市名稱屬性
        if lower_limit != '':
            self.lower_limit = lower_limit
        else:
            self.lower_limit = '0'
        if upper_limit != '':
            self.upper_limit = upper_limit
        else:
            self.upper_limit = '100000'

    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass

# 排序方式
class Arrangement():
    def __init__(self, sort_order, sort_condition):    
        self.sort_order = sort_order # 資料顯示排序
        self.sort_condition = sort_condition # 資料顯示排序指標

    def sortOrder(self):
        if self.sort_order == "▼":
            return 1
        elif self.sort_order == "▲":
            return -1
        else:
            return 1

    def sortCondition(self):
        if self.sort_condition == "價格":
            return "price_value"
        elif self.sort_condition == "評價":
            return "star_value"
        else:
            return "price_value"


# KLOOK客路網站
class Klook(Website):
        
    #設置城市ID位置(若要搜尋國外的，需先設置該地點ID)    
    def city_id(self):
        city_id = {"台北":"19","新北":"6488","桃園":"4737","新竹":"27456","台中":"25","嘉義":"436", \
                   "南投":"25303","台南":"164","高雄":"22","屏東":"23","台東":"47","花蓮":"20","宜蘭":"42", \
                  "澎湖":"43","金門、馬祖":"165"}        
        
        return city_id[self.city_name]
        
    def scrape(self):       
 
        result = []  # 回傳結果
        
        if self.city_name:  # 如果城市名稱非空值
 
            # 取得傳入城市的所有一日遊票券
            
            response = requests.get(f"https://www.klook.com/zh-TW/search/?query=一日遊&city_id={self.city_id()}&start=1")
            soup = BeautifulSoup(response.text, "lxml")
            
            
            # 取得票券卡片(Card)元素
            activities = soup.find_all("div",{"class":"m_justify_list m_radius_box act_card act_card_sm a_sd_move j_activity_item js-item"})
            
            
            for activity in activities:
                # 票券名稱
                title = activity.find("a", {"class": "title"}).text.strip()
                if self.city_name not in title:
                    continue
                
                # 票券詳細內容連結
                link =activity.find("a", {"target": "_blank"}).get("href")
                
                # 票券價格
                price = activity.find("span", {"class": "latest_price"}).text.strip()
                # 將文字及標號過濾以排序
                price_value = int(re.sub("\D","",price))
                
                # 最早可使用日期
                booking_date = activity.find("span", {"class": "g_right j_card_date"}).get("data-serverdate")
                booking_date = booking_date[0:booking_date.index(" ")]
                # 評價
                if activity.find("span", {"class": "t14 star_score"}):
                    star = activity.find("span", {"class": "t14 star_score"}).text
                    # 將文字及標號過濾以排序
                    star_value = int(re.sub("\D","",star))
                else :
                    star = "無"
                    star_value = 0

                if ((price_value >= int(self.lower_limit)) and (price_value <= int(self.upper_limit))):
                	result.append(
                    	dict(title=title, link=link, price=price, price_value=price_value, booking_date=booking_date, star=star, star_value=star_value, source="https://cdn.klook.com/s/dist_web/assert/desktop/imgs/favicon-098cf2db20.png"))
 
        return result



# KKday網站
class Kkday(Website):

    def scrape(self):

        result = []  # 回傳結果

        loc_dict_kkday = {'台北': 'A01-001-00001'}

        if self.city_name:  # 如果城市名稱非空值

            # 取得傳入城市的所有一日遊票券
            response = requests.get("https://www.kkday.com/zh-tw/product/productlist/?city=A01-001-00001&cat=TAG_4_4&sort=pasc")
                # =pasc 價格由低到高
                #f"https://www.kkday.com/zh-tw/product/productlist/?city={loc_dict_kkday.get(self.city_name)}&cat=TAG_4_4&sort=pasc")

            # 資料
            activities = response.json()["data"]

            for activity in activities:

                # 票券名稱
                title = activity["name"]

                # 票券詳細內容連結
                link = activity["url"]

                # 票券價格
                price = f'NT$ {int(activity["price"]):,}'

                # 最早可使用日期
                booking_date = datetime.strftime(datetime.strptime(
                    activity["earliest_sale_date"], "%Y%m%d"), "%Y-%m-%d")

                # 評價
                star = str(activity["rating_star"])[
                    0:3] if activity["rating_star"] else "無"

                if ((price_value >= int(self.lower_limit)) and (price_value <= int(self.upper_limit))):
                    	dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="https://cdn.kkday.com/m-web/assets/img/favicon.png")

        return result

# Eztravel網站
class Eztravel(Website):

    def scrape(self):

        result = []  # 回傳結果

        if self.city_name:  # 如果城市名稱非空值

            # 取得傳入城市的所有一日遊票券
            loc_dict = {'基隆': "KEE", '台北': 'TPE', '桃園': 'TA1', '新竹': 'HSZ', '苗栗': 'MI1', '台中': 'TXG', '彰化': 'ZH1', '南投': 'NA0',
             '雲林': 'YU1', '嘉義': 'CYI', '台南': 'TNN', '高雄': 'KHH', '屏東': 'PIF', '宜蘭': 'YI0', '花蓮': 'HUN', '台東': 'TTT', '澎湖': 'MZG'}

            if loc_dict.get(self.city_name) != "None":

                loc = loc_dict.get(self.city_name)
                url = "https://activity.eztravel.com.tw/taiwan/results/" + loc + "/N5?keywords="
                driver.get(url)
                response = driver.page_source
                soup =  BeautifulSoup(response, "lxml")

                activities = soup.find_all("div", {"class" : "goods-class clearfix w308"})


                for activity in activities:

                    time.sleep(0.5)

                    # 票券名稱
                    title = activity.find("h4", {"class": "tkt-title"}).getText().strip()
 
                    # 票券詳細內容連結
                    link = "https://activity.eztravel.com.tw/taiwan/introduction/" + activity.get("data-prodno")
 
                    # 票券價格
                    price = activity.find("span", {"data-bind": "text: product.formattedMinSitePrice()"}).getText().strip()
                    # 將文字及標號過濾以排序
                    price_value = int(re.sub("\D","",price))

                    # 評價
                    star = "無"
                    star_value = 0

                    if ((price_value >= int(self.lower_limit)) and (price_value <= int(self.upper_limit))):
                    	result.append(dict(title=title, link=link, price=price, price_value=price_value, star=star, star_value=star_value,source="https://static.cdn-eztravel.com/assets/images/common/logo.jpg"))
                 

                #driver.quit()
            return result