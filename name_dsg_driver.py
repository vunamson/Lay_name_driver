import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Cấu hình Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Lay Name Trên Driver\Lay_name_driver\credentials.json", scope)
client = gspread.authorize(creds)

# Mở Sheet cần thao tác
sheet = client.open_by_key("1nksL0jVnLMyw3Hy7MnjaGpLz0NF6OR955uI0tYvLaOs").sheet1  # Sheet đầu tiên

# Lấy tất cả URL từ cột A
urls = sheet.col_values(1)  # Bắt đầu từ dòng 1

# Cấu hình trình duyệt ẩn danh bằng undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)

# Duyệt từng URL
for index, url in enumerate(urls):
    if not url.startswith("http"):
        continue  # Bỏ qua dòng trống hoặc không hợp lệ

    print(f"🔗 Đang xử lý dòng {index + 1}: {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ndfHFb-c4YZDc-Wrql6b-V1ur5d"))
        )
        name_element = driver.find_element(By.CLASS_NAME, "ndfHFb-c4YZDc-Wrql6b-V1ur5d")
        name_text = name_element.text.strip()

        # Ghi vào cột D (tức là cột số 4), dòng tương ứng
        sheet.update_cell(index + 1, 4, name_text)
        print(f"✅ Ghi thành công: {name_text}")
        time.sleep(2)

    except TimeoutException:
        print(f"❌ Không tìm thấy tên ở dòng {index + 1}")
        sheet.update_cell(index + 1, 4, "Không tìm thấy")
    except Exception as e:
        print(f"⚠️ Lỗi dòng {index + 1}: {e}")
        sheet.update_cell(index + 1, 4, "Lỗi")

driver.quit()
print("🎉 Hoàn tất!")
