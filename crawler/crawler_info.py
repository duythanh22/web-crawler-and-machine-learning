
import time
import os.path
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver

# Khởi tạo trình duyệt
driver = webdriver.Edge()
driver.get("https://xe.chotot.com/mua-ban-oto")
time.sleep(0.5)

# click đóng thông báo đăng tin khi mở web
button_popup = driver.find_element(By.CLASS_NAME, 'aw__s13upwxx')
button_popup.click()
time.sleep(0.5)

# Đọc tất cả các dòng trong file links.txt
links = []
with open('raw/links.txt', 'r') as file:
    links = file.readlines()

# Hàm lấy thông tin
def find_value_by_itemprop_1(driver, itemprop):
    try:
        element = driver.find_element(By.CSS_SELECTOR, f'a[itemprop="{itemprop}"].AdParam_adParamValue__IfaYa')
        return element.text
    except:
        return None

def find_value_by_itemprop(driver, itemprop):
    try:
        element = driver.find_element(By.CSS_SELECTOR, f'[itemprop="{itemprop}"]')
        return element.text
    except:
        return None

list_car = []
# Lặp qua các link trong file links.txt
link_start = 1
link_end = 100
for link in links[15401:15500]:
    # Truy cập đến sản phẩm tương ứng với link
    driver.get(link.strip())

    # Click vào button để hiện toàn bộ thông tin
    try:
        button_hidden = driver.find_element(By.CLASS_NAME, 'styles_button__SVZnw')
        button_hidden.click()
        time.sleep(0.5)
    except:
        pass

    # Lấy dữ liệu các đặc tính của sản phẩm
    price = None    # giá
    try:
        price = driver.find_element(By.CSS_SELECTOR, 'span[itemprop="price"]').text
    except:
        pass
    car_brand = find_value_by_itemprop_1(driver,'carbrand')             # hãng
    car_model = find_value_by_itemprop_1(driver,'carmodel')             # dòng xe
    mf_date = find_value_by_itemprop(driver,'mfdate')                   # năm sx
    mileage_v2 = find_value_by_itemprop(driver, 'mileage_v2')           # số km
    condition_ad = find_value_by_itemprop(driver,'condition_ad')        # tình trạng
    gearbox = find_value_by_itemprop(driver,'gearbox')                  # hộp số
    fuel = find_value_by_itemprop(driver,'fuel')                        # nhiên liệu
    carorigin = find_value_by_itemprop(driver,'carorigin')              # xuất xứ
    cartype = find_value_by_itemprop(driver,'cartype')                  # kiểu dáng
    carseats = find_value_by_itemprop(driver,'carseats')                # số chỗ
    veh_warranty_policy = find_value_by_itemprop(driver,'veh_warranty_policy')      # bảo hành
    time.sleep(0.5)

    list_car.append([price, car_brand, car_model, mf_date, mileage_v2, condition_ad, gearbox,
                     fuel, carorigin, cartype, carseats, veh_warranty_policy])
    print(price, car_brand, car_model, mf_date, mileage_v2, condition_ad, gearbox,
          fuel, carorigin, cartype, carseats, veh_warranty_policy)

# Đóng trình duyệt
driver.quit()

df_car = pd.DataFrame(list_car, columns=['Price', 'CarBrand', 'CarModel', 'MfgDate', 'Mileage',
                                         'Condition', 'GearBox', 'Fuel', 'CarOrigin',
                                         'CarType', 'CarSeats', 'WarrantyPolicy'])
print(df_car)


path = 'raw/'
file_path = os.path.join(path, 'car_raw.csv')

# Kiểm tra xem tệp CSV đã tồn tại không
if os.path.isfile(file_path):
    df_car = pd.read_csv(file_path)
else:
    df_car = pd.DataFrame(columns=['Price', 'CarBrand', 'CarModel', 'MfgDate', 'Mileage',
                                   'Condition', 'GearBox', 'Fuel', 'CarOrigin',
                                   'CarType', 'CarSeats', 'WarrantyPolicy'])

# Tạo DataFrame mới từ list_car
df_new = pd.DataFrame(list_car, columns=['Price', 'CarBrand', 'CarModel', 'MfgDate', 'Mileage',
                                         'Condition', 'GearBox', 'Fuel', 'CarOrigin',
                                         'CarType', 'CarSeats', 'WarrantyPolicy'])

# Ghi dữ liệu vào tệp CSV
df_new.to_csv(file_path, index=False, mode='a', header=not os.path.isfile(file_path), encoding='utf-8-sig')

