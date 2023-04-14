from selenium import webdriver
import bs4
import requests
import os
import time

# Creating a directory to save images
folder_name = "images"
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


def download_image(url, folder_name, num):

    response = requests.get(url)

    # wb (write binary) opens the file in binary format for writing
    if response.status_code==200:
        with open(os.path.join(folder_name, str(num)+ ".jpg"), "wb") as file:
            file.write(response.content)

chromeDriverPath = "/home/akshay/Desktop/tim-scraper/chromedriver"
driver = webdriver.Chrome(chromeDriverPath)

searchUrl = "https://www.google.com/search?q=car+road+images&sxsrf=APwXEdeGFQR-JosTtFkQHgkpJSAjeqOShQ:1681381166830&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiAsrT50Kb-AhXyTmwGHWhlAGMQ_AUoAXoECAEQAw&biw=946&bih=964&dpr=1"

driver.get(searchUrl)


# This is what xpath looks like of an element
# //*[@id="islrg"]/div[1]/div[50]
# to replicate, right click an element from DOM, Copy > Copy xpath
# you can use it like
# driver.find_element("xpath",'//*[@id="islrg"]/div[1]/div[3]/a[1]/div[1]/img').click()
a = input("Waiting....")

driver.execute_script("window.scrollTo(0,0);")

page_html = driver.page_source

pageSoup = bs4.BeautifulSoup(page_html, "html.parser")
# print(pageSoup.prettify())

containers = pageSoup.find_all("div", {"class" : "isv-r PNCib MSM1fd BUooTd"})

# print(len(containers))


for i in range(1, len(containers)+1):
    if i % 25 == 0:
        continue
    xPath = f'//*[@id="islrg"]/div[1]/div[{i}]'

    # Here is what the code after this is trying to do
    # We will grab image xpath and also preview image xpath
    # If they are the same, that means the images is not loaded
    # when they differ, we will comclude that the image is now loaded and is high resolution

    # Grabbing XPath of the preview image

    # I have copied 2 xPaths and compared them to decide where to put "i"
    # //*[@id="islrg"]/div[1]/div[23]/a[1]/div[1]/img
    # //*[@id="islrg"]/div[1]/div[7]/a[1]/div[1]/img
    # here 7 and 23 are the difference. Which means that is the thing to iterate over

    previewImageXPath = f'//*[@id="islrg"]/div[1]/div[4]/a[1]/div[1]/img'
    previewImageElement = driver.find_element("xpath", previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    # print(previewImageURL)

    # CLicking on image container
    driver.find_element("xpath", xPath).click()

    timeStarted = time.time()

    while True:
        imageElement = driver.find_element("xpath", '//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div[2]/div[1]/a/img[1]')
        imageURL = imageElement.get_attribute("src")

        if imageURL != previewImageURL:
            print("Full res image", imageURL)
            break

        else:
            # making timeout so image will get some time to download
            currentTime = time.time()

            if currentTime -timeStarted > 10:
                print("Downloading lower resolution image and moving to next one")
                break

    try:
        download_image(imageURL, "images", i)
        print(f"Downloaded element {i} of the total {len(containers+1)}. Image URL is : {imageURL}")
    except:
        print(f"Could not dpwnload image {i}. Procedding to next one")
    