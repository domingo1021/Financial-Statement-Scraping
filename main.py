from DataLoader import InputLoader
from URLScraping import URLScrape, URLScrappingList
import time
from ipaddress import ip_address
import csv
import tkinter as tk
from tkinter import filedialog

if __name__ == '__main__':
    # root = tk.Tk()
    # root.withdraw()
    # file_path = filedialog.askopenfilename()
    start = time.time()
    loader = InputLoader("./input/測試檔.csv")
    scrape_list = URLScrappingList(loader)
    scrape_list.scraps_all()
    # proxies = scrape_list.get_free_proxies()
    end = time.time()
    runtime = start - end
    print(scrape_list.get_output_df())
    print(runtime)

    # for i in URLScrape.get_keywords_standard():
    #     print(type(i))
    #     print(i)


