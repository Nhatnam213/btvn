from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Khởi tạo một danh sách trống để lưu trữ các liên kết
all_links = []
musician_links = []
d = pd.DataFrame({'name of the band': [], 'active years': []})

# Mở trang Wikipedia
driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/Lists_of_musicians#A"

try:
    # Mở web
    driver.get(url)
    # Chờ load trang 3s
    time.sleep(3)
    # Lấy các phần tử <ul.
    ul_tags = driver.find_elements(By.TAG_NAME, "ul")
    print({len(ul_tags)})

    # chọn thẻ ul thứ 22
    ul_musicians = ul_tags[21]

    # Get all <li> elements within the selected <ul>
    li_tags = ul_musicians.find_elements(By.TAG_NAME, "li")
    print({len(li_tags)})

    # Collect all URLs of the musicians
    links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
    all_links.extend(links)

except Exception as e:
    print(f"Error: {e}")

# Close the driver after collecting links
driver.quit()

# Access the first musician link from all_links
artists_driver = webdriver.Chrome()
artists_driver.get(all_links[0])

# Wait for 2 seconds
time.sleep(2)

try:
    # Find all <ul> elements on the musician's page
    ul_artist_tags = artists_driver.find_elements(By.TAG_NAME, "ul")
    print({len(ul_artist_tags)})

    # Chọn phần tử ul thứ 25
    ul_artist = ul_artist_tags[24]

    # Lấy tất cả các phần tử <li> (tên/liên kết nhạc sĩ)
    li_artist = ul_artist.find_elements(By.TAG_NAME, "li")
    print({len(li_artist)})

    # Thu thập tất cả các liên kết nhạc sĩ
    links_artist = [artist_tag.find_element(By.TAG_NAME, "a").get_attribute("href") for artist_tag in li_artist]
    musician_links.extend(links_artist)

except Exception as e:
    print(f"Error: {e}")

# Close the artist driver
artists_driver.quit()

# Thông tin chi tiết
for link in musician_links:
    print({link})
    try:
        # Khởi tạo trình điều khiển Chrome mới cho mỗi trang nhạc sĩ
        driver = webdriver.Chrome()
        driver.get(link)
        time.sleep(2)

        # Lấy tên nhạc sĩ/ban nhạc
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lấy thời gian hoạt động của  nhạc sĩ/ban nhạc
        try:
            year_element = driver.find_element(By.XPATH,'//span[contains(text(),"Years active")]/parent::*/following-sibling::td')
            year = year_element.text
        except:
            year = ""

        # # Tạo dictionary thông tin của nhạc sĩ/ ban nhạc
        musician = {'name of the band': name, 'active years': year}

        # Chuyển dictionary thành DataFrame
        musician_df = pd.DataFrame([musician])
        d = pd.concat([d, musician_df], ignore_index=True)

        # Đóng web driver
        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

# Print the DataFrame
print(d)

# Lưu dataframe vào file Excel
file_name = 'C:/Project/musicians.xlsx'
d.to_excel(file_name, index=False)
print('DataFrame is written to Excel file successfully.')
