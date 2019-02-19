from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib
import os
import random
import sys

dccon_name = sys.argv[1]

options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36")
options.add_argument("--user-data-dir=C:\\Users\\ayh07\\AppData\\Local\\Google\\Chrome\\User Data\\Default")  # �߰�
#options.add_argument('--headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
driver.get("https://dccon.dcinside.com/hot/1/title/"+dccon_name)
#first, go to dccon search page
page_idx = 1
#second, get dccon lists
dccon_list = driver.find_elements_by_class_name("link_product")
dccon_idx = 0
for dccon in dccon_list :
    dccon_title = dccon.find_element_by_class_name("dcon_name").get_attribute("innerHTML")
    print(str(dccon_idx) + " " + dccon_title)


print("Page Index : " + str(page_idx))
print("원하는 인덱스의 번호를 입력하세요.")
print("이전 페이지를 탐색하려면 P을 입력하세요.")
print("다음 페이지를 탐색하려면 N을 입력하세요.")
print("종료하시려면 X를 입력하세요")
user_choice = input("입력 : ")
if str(user_choice).isdigit() :
    #check user selection is bigger than list size
    if int(user_choice) > len(dccon_list) :
        
    #user selected dccon
    #so parse it
    driver.get(dccon_list[int(user_choice)].get_attribute("href"))
    imgSets = driver.find_elements_by_class_name("img_dccon")
    title = driver.find_element_by_class_name("font_blue").get_attribute("innerHTML")
    index = 0
    for span in imgSets :
        img = span.find_element_by_tag_name("img")
        src = img.get_attribute("src")
        src = str(src).replace('dcimg5','image')

        folder = ""
        if not os.path.exists(title) :
            folder = title
            os.makedirs(title)
        else :
            folder = title+str(random.randrange(0,100))
            os.makedirs(folder)
        
        img_file = urllib.request.urlopen(src)
        f = open("./"+folder+"/"+str(index)+".jpg",'wb')
        f.write(img_file.read())
        urllib.request.urlretrieve(src, str(index)+".jpg")
        print(img.get_attribute("alt"))
        index = index +1
else :
    #user selected search next page.
    #there are three number of cases:
    #first, there are no more page(reached end of pages)
    #second, more page available
    #third, no pages in there (only 1 page)
    #so, first we should check we can go to next page
    paging_box = driver.find_element_by_class_name("bottom_paging_box")
    #check a tag is available
    current_page = paging_box.find_element_by_tag_name("em").get_attribute("innerHTML")
    page_list = paging_box.find_elements_by_tag_name("a")
    #if size is 0, no pages in there
    #if size is bigger than 1, check more page is available
