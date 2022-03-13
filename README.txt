## RPA financial statenent scraping
<h1>This is my first project in E.SUN FHC RPA track.</h1>
<br>Using Python selenium, HTTP requests, and Pandas to help departments to scrape financial statement online.
<br>The reptile object of this project is Taiwan Stock Exchange (台灣證交所公開資訊觀測站, twse).
<br>ps: Please set a Time interval (which is time.sleep(10) in Python) about ten seconds between every time of scrape in order to avoid anti-scraping.
<br>
#### Step to utilize this project
Step 1. Prepare .csv file as input to this project. For the format of csv file, please refer to ./input/測試檔.csv as an example.
<br>
Step 2. Set your input csv file in InputLoader object within main.py to initialize an input object.
<br>
Step 3. Type "virtual\Scripts\activate" in terminal to get access to virtual environment.
<br>
Step 4. Type "python main.py" in terminal to run the project.
<br>
Step 5. After scraping financial statement, all the pdf files of statement will be stored in a directory belongs to each company respectively,
<br>and the directory name is set as ticker number of each stock in Taiwan stock market. 
Step 6. User also can get an "output.csv" in ./output/輸出_{input file name}.csv to get access to information of an individual scrape.