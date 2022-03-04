import os
import time
import requests

from typing import List
# Module for scraping
from urllib import response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
確定適用於其他股票
將URL Processing寫成是function
"""
class URLScrape:
    """
    1. Process user demand 
    2. need to return stored-drive path for PDF files and URL for online PDF, which user can click immediately
    """
    def __init__(self, co_id:str, year:str, driver="Chrome") -> None:
        self.co_id = co_id
        self.year = year
        assert driver=="Chrome", "We still haven't provided services for other drivers, use Chrome !"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.__financial_statement_title = None
        self.__file_path = None
        self.__target_url = None
        self.__have_scraped = False

    @property
    def target_url(self)-> str:
        return self.__target_url

    @property
    def file_path(self)-> str:
        return self.__file_path  

    @property
    def financial_statement_title(self)-> str:
        return self.__financial_statement_title
    
    @property
    def have_scraped(self):
        return self.__have_scraped
    
    def get_historical_data(self)-> tuple:
        assert self.__have_scraped == True, "Financial statement haven't been scraped."
        return (self.__financial_statement_title, self.__file_path, self.__target_url)

    def scrape(self)-> None:
        if self.__have_scraped:
            """
            已經爬過, 提供使用者歷史資訊 (get_property()),
            並且 return None 跳出 method
            """
            print("The url haved been scraped.")
            return None
        
        self.driver.get("https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id="+self.co_id+"&year="+self.year+"&seamon=&mtype=A&")
        # driver.find_element_by_xpath("/html/body/center/form/table[2]/tbody/tr[9]/td[8]/a").click()

        """First page"""
        # Receive 10 elements, which is different kind of financial statements. First index is column header, need to be skipped
        # Try first one to download pdf file
        """可以用index控制要哪一種的PDF檔"""
        table = self.driver.find_elements(By.XPATH,"/html/body/center/form/table[2]/tbody/tr")[1]
        # print(len(table))
        url_link = table.find_element(By.PARTIAL_LINK_TEXT, ".pdf")
        self.__financial_statement_title = url_link.text
        url_link.click()
        # time.sleep(2)

        """Second Page (new windows) --> Need to switch to new windows"""
        # 獲得當前所有開啟的視窗的控制程式碼，只適用於出現的第二個視窗 --> 可以用list的方法進行改進 (ex:取最後一個 all_handles[-1])
        search_windows = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != search_windows:
                self.driver.switch_to.window(handle)
                print(self.driver.current_url + "\tURL has changed")
            else:
                print('當前頁面url: %s'%self.driver.current_url)

        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, self.__financial_statement_title)))
        pdf = self.driver.find_element(By.LINK_TEXT, self.__financial_statement_title)
        pdf.click()

        """Third Page, Financial statement Page"""
        #Download the PDF file here
        self.__target_url = self.driver.current_url
        output_dir = os.path.join(os.getcwd(), self.co_id)
        print("hello")
        if not os.path.exists(output_dir):
            print(os.path.exists(output_dir))
            print(output_dir)
            os.makedirs(output_dir)
        response = requests.get(self.__target_url)
        if response.status_code == 200:
            self.__file_path = os.path.join(output_dir, os.path.basename(self.__target_url))
            with open(self.__file_path, "wb") as f:
                f.write(response.content)            
        # time.sleep(10)

        #Set have_scraped as True
        print("Download success !")
        self.__have_scraped = True

        """ Shutdown Chrome drive """
        self.driver.quit()

    
class URLScrappingList:
    """
    1. Storing all the URLScrape
    2. Present all the information of URLScrape
    3. Remember to fetch "have_scraped" from URLScrappingList Object
    """
    def __init__(self, ) -> None:
        pass

if __name__ == '__main__':
    # 輸入端之後要改DataLoader. (pd.read_csv(./....csv))
    scrape = URLScrape("6269", "109")
    scrape.scrape()
    for info in scrape.get_historical_data():
        print(info)
    #可以思考一下要在哪裡控制已經做過（感覺是要在URLScrapList裡面）... 或者是輸入多個年度
    #Q1 如果該年度沒有出現怎麼辦 ?
    #Q2 怎麼選擇想要的財報類型 
    # 方法一: 先將頁面上今年的財報站存進List, 再找出使用者想要的那一個, 若沒有找到的話先回傳查無此資料, 並在附註攔跟使用者說: 去檔案的xxx找找看 (放備註)
    #Q3 處理查無此資料
