from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt
driver = webdriver.Chrome()

#lấy đường liên kết
driver.get("https://xe.chotot.com/mua-ban-oto")
time.sleep(0.5)

# Tìm phần tử chứa thông tin cần trích xuất bằng class name
element = driver.find_element(By.CLASS_NAME, 'commonStyle_adTitle__g520j ')

# Trích xuất văn bản từ phần tử
info_text = element.text
print(info_text)
