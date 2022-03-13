<h2>RPA financial statenent scraping</h2>
To help deparments who need huge numbers of financial statement, we build this project to scrape finanical statement online.
<br>



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

2. Set your input csv file path in `InputLoader` to initialize an input object, ex:  

```python
InputLoader("./input/測試檔.csv")
```

3. Type cmd command below to activate virtual environment.

```bash
virtual\Scripts\activate
```

4. Type command below in terminal to run the project.

```bash
python main.py
```

5. After scraping financial statement, all the financial statement like 
[`2330_108年第四季中文版合併財報.pdf`](https://github.com/domingo1021/Financial-Statement-Scraping/blob/main/2330/2330_108年第四季中文版合併財報.pdf) will be stored in a directory belongs to each company respectively. And the **directory name** is set as ticker number `2330` of each stock in Taiwan stock market. 

6. User also can get an [`output.csv`](https://github.com/domingo1021/Financial-Statement-Scraping/tree/main/output) in  `./output/輸出_{Input file name}` to get access to information of an individual scrape.



### Reminder
Please set a **Time interval** (which is `time.sleep(10)` in Python) about ten seconds between every time of scrape in order to **avoid anti-scraping**.
