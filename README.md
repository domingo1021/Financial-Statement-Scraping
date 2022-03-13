<h2>RPA financial statement scraping</h2>

To help deparments who need huge numbers of financial statement, we build this project to **scrape finanical statement online** .


### Reptile target
The reptile target of this project is Taiwan Stock Exchange (台灣證交所公開資訊觀測站, twse).
<br>



### Package used
Mainly using `Python` programming language packages below to help departments to scrape financial statement online.
- **Python selenium**
- **HTTP requests**
- **Pandas**



### Step to utilize this project, Fist stage
1. Prepare .csv file as input to this project. For the format of csv file, please refer to [`測試檔.csv`](https://github.com/domingo1021/Financial-Statement-Scraping/blob/main/input/%E6%B8%AC%E8%A9%A6%E6%AA%94.csv)

2. Input some information about the financial statement you want to search for.  

  - **Option (1)**: Set your input csv file path directly in `InputLoader` to initialize an input object as below:

  ```python
  InputLoader("./input/測試檔.csv")
  ```

  - **Option (2) --> More flexible**: Using `tkinter` to select .cvs file you want.

  ```python
  import tkinter as tk
  from tkinter import filedialog

  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(initialdir = "./input")

  loader = InputLoader(file_path)
  ```

3. Type cmd command lines below to prepare for required environment.

     - Building virtual environment: `python -m venv virtual`

     - Activate virtual environment: `virtual\Scripts\activate`

     - Install requirements package for this project: `pip -r requirements.txt`

4. Type `python main.py` in terminal to run the project.

5. After scraping financial statement, all the financial statement like 
[`2330_108年第四季中文版合併財報.pdf`](https://github.com/domingo1021/Financial-Statement-Scraping/blob/main/2330/2330_108年第四季中文版合併財報.pdf) will be stored in a directory belongs to each company respectively. And the **directory name** is set as ticker number `2330` of each stock in Taiwan stock market. 

6. User also can get an [`output.csv`](https://github.com/domingo1021/Financial-Statement-Scraping/tree/main/output/輸出_測試檔.csv) in  `./output/輸出_{Input file name}` to get access to information of an individual scrape.



### Result
For testing file, we imitate some real time condition, and provide **4 real demands file** and **6 fake demands** (which are some **exceptions** we want to catch) in [`測試檔.csv`](https://github.com/domingo1021/Financial-Statement-Scraping/blob/main/input/%E6%B8%AC%E8%A9%A6%E6%AA%94.csv) file.

This project Only use **1~2 minutes depends on your device** to get correct answer!


### Reminder
1. The chrome.exe software is for **Chrome 99 version**, make sure you have upgraded Chrome version before using this project.
2. Please set a **Time interval**, which is `time.sleep(10)` in Python, about ten seconds between every time of scrape in order to **avoid anti-scraping**.
