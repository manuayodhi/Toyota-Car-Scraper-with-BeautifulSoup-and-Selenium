from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Extracting used Toyota cars listings from Cars24 for Mumbai

driver = webdriver.Chrome()
driver.get("https://www.cars24.com/buy-used-toyota-cars-mumbai/?sort=bestmatch&serveWarrantyCount=true&search=toyota&listingSource=Search_LP&storeCityId=2378")

elems = driver.find_elements(By.CLASS_NAME, "styles_wrapper__b4UUV")
print(f"{len(elems)} items found")

query = "car"
file = 0

for elem in elems:
    d = elem.get_attribute("outerHTML")
    with open(f"data/{query}_{file}.html","w", encoding="utf-8") as f:
        f.write(d)
        file += 1
    time.sleep(2)
driver.close()