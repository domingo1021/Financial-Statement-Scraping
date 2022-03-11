import os
import time
import pandas as pd
import requests
import json
import ast

from fake_useragent import UserAgent
from DataLoader import InputLoader
from typing import List
# Module for scraping
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#exception handling
from selenium.common.exceptions import NoSuchElementException, TimeoutException
class URLScrape:
    """
    1. Process user demand 
    2. need to return stored-drive path for PDF files and URL for online PDF, which user can click immediately
    """
    __YEAR = time.strftime('%Y', time.localtime())
    __SEASON = ["第一季", "第二季", "第三季", "第四季"]
    __FINANCIAL_STATEMENT_TYPE = ["個體", "合併"]
    __LANGUAGE = ["中文版", "英文版"]

    def __init__(self, co_id:str, year:str, season:str, type_:str, language, driver="Chrome") -> None:
        """
        Constructor
        input: keywords, (後續DataLoader完成可以直接使用物件做為輸入, 取其參數)
        co_id:str, year:str, season:str, type:str
        """
        self.co_id = co_id
        self.year = year
        self.season = season
        self.type_ = type_
        self.language = language
        # self.options = Options()
        # self.options.add_argument("--incognito")           #開啟無痕模式
        # self.options.add_argument("--headless")
        self.driver = driver
        self.__basename = None
        self.__financial_statement_title = None
        self.__file_path = None
        self.__target_url = None
        self.__return_message = "unsuccess"        
        self.__result_status = None
        self.__output_format = ["公司代碼", "年度", "季別", "個體/合併", "語言", "檔案名稱", "檔案路徑", "財報網站連結", "結果"]

    @property
    def target_url(self)-> str:
        return self.__target_url

    @property
    def file_path(self)-> str:
        return self.__file_path  

    @property
    def basename(self)-> str:
        return self.__basename

    @property
    def financial_statement_title(self)-> str:
        return self.__financial_statement_title

    @property
    def result_status(self):
        return self.result_status

    @property
    def return_message(self)-> str:
        return self.__return_message

    @property
    def output_format(self):
        return self.__output_format
    
    @staticmethod
    def is_financial_institute(url:str)-> bool:
        r = requests.get(url)
        if "本網站提供查詢金融控股公司已公開發行之子公司各季財務報告" in r.text:
            return True
        else: return False

    @classmethod
    def get_keywords_standard(cls):
        # list(range(cls.__MAX_TICKER)), cls.__YEAR,
        return (cls.__YEAR, cls.__SEASON, cls.__FINANCIAL_STATEMENT_TYPE, cls.__LANGUAGE)
    
    @property
    def keywords_valid(self):
        """
        check whether "self.__keywords" valid, usually used when choosing financial statement.
        """
        valid = False
        if (self.__YEAR > URLScrape.get_keywords_standard()[0]):
            self.__result_status = "財報「年度」錯誤"
        elif (self.season not in URLScrape.get_keywords_standard()[1]):
            self.__result_status = "財報「季度」錯誤"
        elif (self.type_ not in URLScrape.get_keywords_standard()[2]):
            self.__result_status = "請選擇「個體」或「合併」財報"
        elif (self.language not in URLScrape.get_keywords_standard()[3]):
            self.__result_status = "請選擇「中文版」或「英文版」"
        else: 
            valid = True
        return valid

    def get_output_df(self)-> tuple:
        return pd.DataFrame(data= [[self.co_id, self.year, self.season, self.type_, self.language, self.__basename, self.__file_path, self.__target_url, self.__result_status]], 
                            columns= self.output_format) 

    def request_first_page_content(self, url: str):
        """
        Store tables of content into DataFrame. Help to be convenient to check content.
        """
        request = requests.get(url)
        df = pd.read_html(request.text)
        return df

    def match_user_need(self,elements: List[WebElement])-> int:
        """
        Matching financial statement based on user need, return the desired index.
        If not match, return not found.
        return the element matching requirement
        """
        if self.language == "英文版":
            for web_element in elements[1:]:
                web_text = web_element.text
                if "英文版" in web_text and self.season in web_text and self.type_ in web_text:
                    return web_element
        else:
            for web_element in elements[1:]:
                web_text = web_element.text
                if "英文版" not in web_text and self.season in web_text and self.type_ in web_text:
                    return web_element


    def scrape(self) -> str:
        # if self.__have_scraped:
        #     """
        #     已經爬過, 提供使用者歷史資訊 (get_property()),
        #     並且 return None 跳出 method
        #     """
        #     print("The url haved been scraped.")
        #     return None
        print(self.co_id)
        if (self.keywords_valid != True):
            self.__return_message="invalid"
            return self.__return_message
        try:
            """Try catch (連接到下方, 都與無法下載、查無資訊相關)"""
            print("started")
            first_page_url = "https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id="+self.co_id+"&year="+self.year+"&seamon=&mtype=A&"
            self.driver.get(first_page_url)
            if URLScrape.is_financial_institute(first_page_url):
                self.driver.find_element(By.XPATH, "/html/body/center/form/table[1]/tbody/tr[2]/td[3]/input").click()

            """First page"""
            # Receive 10 elements, which is different kind of financial statements. First index is column header, need to be skipped
            # use index and variable to check which pdf file to use. 
            elements = self.driver.find_elements(By.XPATH,"/html/body/center/form/table[2]/tbody/tr")
            match_element = self.match_user_need(elements)
            url_link = match_element.find_element(By.PARTIAL_LINK_TEXT, ".pdf")
            self.__financial_statement_title = url_link.text
            url_link.click()
            # try:
            # except NoSuchElementException:
            #     pass

            """Second Page (new windows) --> Need to switch to new windows"""
            # 獲得當前所有開啟的視窗的控制程式碼，只適用於出現的第二個視窗 --> 可以用list的方法進行改進 (ex:取最後一個 all_handles[-1])
            search_windows = self.driver.current_window_handle
            all_handles = self.driver.window_handles
            for handle in all_handles:
                if handle != search_windows:
                    self.driver.close()
                    self.driver.switch_to.window(handle)
                    print("URL has changed")
                else:
                    print('當前頁面url: %s'%self.driver.current_url)

            wait = WebDriverWait(self.driver, 1)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, self.__financial_statement_title)))
            pdf = self.driver.find_element(By.LINK_TEXT, self.__financial_statement_title)
            pdf.click()

            """Third Page, Financial statement Page"""
            #Download the PDF file here
            self.__target_url = self.driver.current_url
            output_dir = os.path.join(os.getcwd(), self.co_id)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            response = requests.get(self.__target_url)
            if response.status_code == 200:
                self.__basename = f"{self.co_id}_{self.year}年{self.season}{self.language}{self.type_}財報.pdf"
                self.__file_path = os.path.join(output_dir, self.__basename)
                with open(self.__file_path, "wb") as f:
                    f.write(response.content)            

            #Set have_scraped as True
            self.__result_status = "下載成功！"
            print("Download success !")
            self.__return_message = "success"

        except TimeoutException as e:
            print("Timeout Exception at "+self.co_id)

        finally: 
            return self.__return_message

    
class URLScrappingList:
    """
    1. Storing all the URLScrape
    2. Present all the information of URLScrape
    """
    def __init__(self, input_object: InputLoader)-> None:
        self.__input = input_object
        self.__result = pd.DataFrame({"公司代碼": None, "年度": None, "季別": None, "個體/合併": None, "語言": None, "檔案名稱": None, "檔案路徑": None, "財報網站連結": None, "結果":None}, index=[0])
        self.user_agent = UserAgent()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")#開啟無痕模式
        self.options.add_argument('--user-agent='+self.user_agent.google )
        # self.options.add_argument('--proxy-server=88.255.102.98:8080')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = self.options)

    # Get free proxies for rotating, if need for anti-scrape. (not use now.)
    def get_free_proxies(self):
        self.driver.get('https://sslproxies.org')

        table = self.driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        headers = []
        for th in thead:
            headers.append(th.text.strip())

        proxies = []
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(len(headers)):
                proxy_data[headers[i]] = tds[i].text.strip()
            proxies.append(proxy_data)
        ip_address_ = []
        port_ = []
        for index ,i in enumerate(proxies): 
            new_x = json.dumps(i,sort_keys=True)
            print(index)
            dic = ast.literal_eval(new_x)
            ip_address_.append(dic["IP Address"])
            port_.append(dic["Port"])
        print(ip_address_)
        print(port_)
        #randomly select (IP address: port) from ip_address_ and port_.
        
        return ip_address_, port_

    def scraps_all(self)-> None:
        for index_task in range(self.__input.num_of_request):
            series = self.__input.df.iloc[index_task ,:]
            co_id, year, season, type_, language= str(series.iloc[0]), str(series.iloc[1]), str(series.iloc[2]), str(series.iloc[3]), str(series.iloc[4])
            # scrape_obj = URLScrape(co_id, year, season, type_, language, self.driver)
            scrape_obj = URLScrape(co_id, year, season, type_, language, self.driver)
            return_message = scrape_obj.scrape()
            print(return_message)
            if return_message != "invalid":
                time_out = 1
                while( not return_message=="success" and (time_out <= 3)):
                    print("rerun")
                    self.driver.close()
                    self.driver.quit()
                    tem_option = webdriver.ChromeOptions()
                    tem_option.add_argument("--incognito") #開啟無痕模式
                    tem_option.add_argument('--user-agent='+self.user_agent.firefox )
                    # tem_option.add_argument('--proxy-server=20.103.234.40:8080')
                    time.sleep(15)
                    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options = tem_option)
                    scrape_obj = URLScrape(co_id, year, season, type_, language, self.driver)
                    return_message = scrape_obj.scrape()
                    time_out += 1
            else:
                pass
            self.__result = pd.concat([self.__result, scrape_obj.get_output_df()])
            time.sleep(10)
        self.driver.quit()
        print("爬蟲結束")
        self.__result = self.__result.iloc[1:].reset_index(drop=True)
        self.__result.to_csv("./output/輸出_"+self.__input.basename, encoding="Big5", index = False)

    def get_output_df(self)-> pd.DataFrame:
        return self.__result