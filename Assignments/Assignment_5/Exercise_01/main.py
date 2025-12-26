from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sunbeaminfo.in/internship")
print("Page Title:", driver.title)

table_div = driver.find_element(By.CLASS_NAME, "table-responsive")
table_body = table_div.find_element(By.TAG_NAME, "tbody")
table_rows = table_body.find_elements(By.TAG_NAME, "tr")

for row in table_rows:
    # print(row.text)
    cols = row.find_elements(By.TAG_NAME, "td")
    info = {
        "Sr.No": cols[0].text,
        "Batch": cols[1].text,
        "Batch Duration": cols[2].text,
        "Start Date": cols[3].text,
        "End Date": cols[4].text,
        "Time": cols[5].text,
        "Fees(Rs.)": cols[6].text
    }
    print(info)

driver.implicitly_wait(5)

driver.quit()