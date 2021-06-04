from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from datetime import datetime
# KLOOK客路網站
class Klook:
    

    def __init__(self, city_name):
        
        self.city_name = city_name
        
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
            
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            
            # 取得十個票券卡片(Card)元素
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
                
                # 最早可使用日期
                booking_date = activity.find("span", {"class": "g_right j_card_date"}).get("data-serverdate")
                booking_date = booking_date[0:booking_date.index(" ")]
                # 評價
                if activity.find("span", {"class": "t14 star_score"}):
                    star = activity.find("span", {"class": "t14 star_score"}).text
                    
                else :
                    star ="無"
                    
 
                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="https://cdn.klook.com/s/dist_web/assert/desktop/imgs/favicon-098cf2db20.png"))
 
        return result
demo = Klook("台中")
print(demo.scrape())