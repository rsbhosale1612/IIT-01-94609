from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()

driver.get("https://sunbeaminfo.in/internship")
print("Page Title:", driver.title)



wait = WebDriverWait(driver, 10)

# element = wait.until(
#     EC.element_to_be_clickable(
#         (By.XPATH, "//a[contains(text(),'Available Internship Programs')]")
#     )
# )
# element.click()

element = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='#collapseSix']")
    )
)
element.click()

# element = wait.until(
#     EC.element_to_be_clickable(
#         (By.CSS_SELECTOR, "a[data-toggle='collapse'][href='#collapseSix']")
#     )
# )
# element.click()



# time.sleep(5)
# collapse = driver.find_element(By.XPATH, "//a[contains(text(),'Available Internship Programs')]")
# collapse.send_keys(Keys.RETURN)
div = driver.find_element(By.ID, "collapseSix")
table_body = div.find_element(By.TAG_NAME, "tbody")
table_rows = table_body.find_elements(By.TAG_NAME, "tr")

print("\nAvailable Internship Programs: ")
for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    info = {
        "Technology": cols[0].text,
        "Aim": cols[1].text,
        "Prerequisite": cols[2].text,
        "Learning": cols[3].text,
        "Location": cols[4].text 
    }
    print(info, end="\n\n")

# driver.implicitly_wait(5)
time.sleep(10)
driver.quit()