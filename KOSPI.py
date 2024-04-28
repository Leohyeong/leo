from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def get_company_info(driver, company_url):
    try:
        # Open the company's page
        driver.get(company_url)

        html = driver.page_source
        # html = requests.get(company_url).text
        soup = BeautifulSoup(html, 'html.parser') # 
        company_name = soup.find('title').text.split(':')[0].strip()

        # Extract financial data
        financial_data = []
        
        etf = f'//*[@id="middle"]/div[1]/div[1]/div/em[2]/span'

        if etf == "ETF개요":
            
            driver.quit()

        else: # Extract the HTML content of the company's page

            # 주가
            xpath_currunt_price = f'//*[@id="content"]/div[5]/table/tbody/tr[1]/td[1]'
            currunt_price = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, xpath_currunt_price))
                )
            if currunt_price:
                financial_data.append(currunt_price.text.strip())  # 
            else:
                financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.
            
            # 당기순이익
            for i in range(1, 5):
                xpath_net_profit = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[3]/td[{i}]'
                net_profit = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, xpath_net_profit))
                )
                # xpath = f'//html/body/div[3]/div[2]/div[2]/div[1]/div[4]/div[1]/table/tbody/tr[3]/td[{1}]'
                # element = soup.find(xpath)
                if net_profit:
                    financial_data.append(net_profit.text.strip())  # 
                else:
                    financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.
                    
            # 부채비율 : 100% 이하
            for i in range(1, 4):
                xpath_debt_ratio = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[7]/td[{i}]'
                debt_ratio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_debt_ratio))
                )
                if debt_ratio:
                    financial_data.append(debt_ratio.text.strip())  # 
                else:
                    financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.

            # 당좌비율 : 100% 이상
            for i in range(1, 4):
                xpath_quick_ratio = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[8]/td[{i}]'
                quick_ratio = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.XPATH, xpath_quick_ratio))
                )
                if quick_ratio:
                    financial_data.append(quick_ratio.text.strip())  # 
                else:
                    financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.

            # 유보율 : 높을수록 좋음
            for i in range(1, 4):
                xpath_reserve_ratio = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[9]/td[{i}]'
                reserve_ratio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_reserve_ratio))
                )
                if reserve_ratio:
                    financial_data.append(reserve_ratio.text.strip())  # 
                else:
                    financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.

            # 미래PER : 10~15이하
            xpath_future_per = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[11]/td[4]'
            future_per = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_future_per))
            )
            if future_per:
                financial_data.append(future_per.text.strip())  # 
            else:
                financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.

            #미래PBR : 1이하면 좋으나 PER 우선
            xpath_future_pbr = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[13]/td[4]'
            future_pbr = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_future_pbr))
            )
            if future_pbr:
                financial_data.append(future_pbr.text.strip())  # 
            else:
                financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.

            #시가배당률 : 시중 금리보단 높은 것
            for i in range(1, 4):
                xpath_dividend_yield = f'//*[@id="content"]/div[4]/div[1]/table/tbody/tr[15]/td[{i}]'
                dividend_yield = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_dividend_yield))
                )
                if dividend_yield:
                    financial_data.append(dividend_yield.text.strip())  # 
                else:
                    financial_data.append("N/A")  # 또는 다른 기본값을 사용할 수 있습니다.
        
    except (TimeoutException, NoSuchElementException):
        for _ in range(19):
                financial_data.append("N/A")

    return company_name, financial_data

def get_kospi_market_cap_rankings():
    # Set up Selenium webdriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening browser window)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    try:
        rankings = []  # To store rankings of companies

        for page in range(1,2):  # Loop through the first 2 pages (each page shows 50 items)

            # Navigate to the Naver Finance website
            url = f"https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page={page}"
            driver.get(url)
            
            # Wait for the table to load
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "contentarea")))

            # Extract the HTML content
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find and parse the table
            table = soup.find('table', {'class': 'type_2'})
            # table = soup.find('table', {'class'})

            if table:
                # Get the rows for the current page
                rows = table.find_all('tr', {'onmouseover': True})
                
                # Extract data for each company
                for row in rows:
                # for row in range(48,51):
                    cols = row.find_all('td')
                    if len(cols) >= 9:
                        company_url = "https://finance.naver.com" + cols[1].find('a')['href']  # Get company's URL
                        company_info = get_company_info(driver, company_url)  # Get company's info from its page
                        rankings.append(company_info)
                
        return rankings
        
    finally:
        # Close the webdriver
        driver.quit()

# Example usage
kospi_rankings = get_kospi_market_cap_rankings()
if kospi_rankings:
    # Create a DataFrame to store the data
    df = pd.DataFrame(columns=['Company','현재 주가',
                               '2021년 당기순이익', '2022년 당기순이익', '2023년 당기순이익', '2024년 당기순이익',
                               '2021년 부채비율', '2022년 부채비율', '2023년 부채비율',
                               '2021년 당좌비율', '2022년 당좌비율', '2023년 당좌비율',
                               '2021년 유보율', '2022년 유보율', '2023년 유보율',
                               '미래PER', '미래PBR',
                               '2021년 시가배당률', '2022년 시가배당률', '2023년 시가배당률'])
    
    # Populate the DataFrame with data
    for company_info in kospi_rankings:
        
        company_name, financial_data = company_info
        new_data = {'Company': company_name, '현재 주가':financial_data[0],
                    '2021년 당기순이익': financial_data[1], '2022년 당기순이익': financial_data[2],'2023년 당기순이익': financial_data[3],'2024년 당기순이익': financial_data[4],
                    '2021년 부채비율': financial_data[5], '2022년 부채비율': financial_data[6],'2023년 부채비율': financial_data[7],
                    '2021년 당좌비율': financial_data[8], '2022년 당좌비율': financial_data[9],'2023년 당좌비율': financial_data[10],
                    '2021년 유보율': financial_data[11], '2022년 유보율': financial_data[12],'2023년 유보율': financial_data[13],
                    '미래PER': financial_data[14], '미래PBR': financial_data[15],
                    '2021년 시가배당률': financial_data[16], '2022년 시가배당률': financial_data[17],'2023년 시가배당률': financial_data[18]
                    }
        new_df = pd.DataFrame([new_data])

        # 기존 DataFrame과 새로운 DataFrame 결합
        df = pd.concat([df, new_df], ignore_index=True)
        df.index = df.index+1
    
    # Save the DataFrame to an Excel file
    filename = "KOSPI200_"
    date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    df.to_excel(filename + date + '.xlsx', index=True)
    print("Excel file saved successfully.")
