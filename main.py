import io
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
from PIL import Image
PATH =  "C:\\Users\\ahpat\\OneDrive\\Desktop\\chromedriver.exe"
wd = webdriver.Chrome(PATH)
def get_images_from_google(wd,delay,max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
    url = "https://www.google.com/search?q=ai/ml+images&rlz=1C1ONGR_enIN1030IN1030&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiEx_r8up_8AhV7-TgGHbl6CtUQ_AUoAXoECAMQAw&biw=1366&bih=657&dpr=1#imgrc=yUNWAEn-medOWM"
    wd.get(url)
    image_urls = set()
    while len(image_urls)<max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME,"n3VNCb KAlRDb")
        for img in thumbnails[len(image_urls):max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME,"n3VNCb KAlRDb")
            for image in images:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print("Found {len(image_urls)}")
    return  image_urls

def download_image(download_path,url,file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open(file_path,"wb") as f:
            image.save(f,"JPEG")
        print("success")
    except Exception as e:
        print("FAILED",e)
urls = get_images_from_google(wd,2,20)
print(urls)
wd.quit()