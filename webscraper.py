import os
import requests
import selenium
from selenium import webdriver
import time


def download_image(url, folder_name, num):
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, str(num) + ".jpg"), "wb") as file:
                file.write(response.content)
        else:
            print("Download Failed")
    except Exception as _e:
        print("Failed Download with e:", _e)


def webscraper(search_url, folder_name, allowLowRes=True):
    chrome_driver_path = r"chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(search_url)
    go = input("Waiting for user input to start...")
    driver.execute_script("window.scrollTo(0,0);")

    count = 0
    elements = driver.find_element_by_class_name("islrc").find_elements_by_tag_name(
        "div"
    )
    for element in elements:
        class_name = element.get_attribute("class")
        if class_name == "isv-r PNCib ViTmJb BUooTd":
            count += 1
            preview_url = element.get_attribute("src")
            element.click()
            time_started = time.time()
            while True:
                image_element = driver.find_element_by_xpath(
                    """//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]"""  # big preview
                )
                image_URL = image_element.get_attribute("src")
                if (
                    (image_URL != preview_url)
                    and ("data:image/jpeg;base64," not in image_URL)
                    and ("https://encrypted-tbn0.gstatic.com" not in image_URL)
                ):
                    download_image(image_URL, folder_name, count)
                    break
                else:
                    current_time = time.time()

                    if current_time - time_started > 10:
                        if "data:image/jpeg;base64," not in image_URL:
                            if allowLowRes:
                                download_image(image_URL, folder_name, count)
                        break
        else:
            continue
