from DataLoader import InputLoader
from URLScraping import URLScrape, URLScrappingList
import time
import tkinter as tk
from tkinter import filedialog

if __name__ == '__main__':
    # Option 1
    # loader = InputLoader("./input/測試檔.csv")
    
    #Option 2
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir = "./input")
    start = time.time()
    loader = InputLoader(file_path)
    scrape_list = URLScrappingList(loader)
    scrape_list.scraps_all()
    # proxies = scrape_list.get_free_proxies()
    end = time.time()
    runtime = end - start
    print(scrape_list.get_output_df())
    print(runtime)



