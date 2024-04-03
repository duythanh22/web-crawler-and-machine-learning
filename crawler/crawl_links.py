from selenium import webdriver
import time
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
driver.get("https://xe.chotot.com/mua-ban-oto")
time.sleep(0.5)


# Ghi các link vào file links.txt
# Mỗi page có 25 sản phẩm tương ứng với 25 link
with open('raw/links.txt', "a", encoding="utf-8") as f:
    page_start = 1
    page_end = 1000
    for i in range(page_start, page_end):
        driver.get("https://xe.chotot.com/mua-ban-oto?page=" + str(i))
        time.sleep(0.5)
        a_elements = []
        a_elements = driver.find_elements(By.CSS_SELECTOR,
                                          "[class='AdItem_adItem__gDDQT']")
        for a in a_elements:
            f.write(a.get_attribute('href') + "\n")

# Đóng trình duyệt
driver.quit()



