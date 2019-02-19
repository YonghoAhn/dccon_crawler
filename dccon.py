from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request
import os
import random
import sys
import re

def init_driver() :
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)

def download(driver, url) :
    return 0

def get_page(driver) :
    return 0

if __name__ == "__main__" :
    #check is url or name
    #if url, go to download
    driver = init_driver()
    if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sys.argv[1]) :
        download(driver, sys.argv[1])
    else :
        dccon_name = sys.argv[1]
        page_idx = 1
        while True:
            driver.get("https://dccon.dcinside.com/hot/" + str(page_idx) + "/title/"+dccon_name)
            #first, go to dccon search page
            #second, get dccon lists
            try :
                dccon_list = driver.find_elements_by_class_name("link_product")
            except Exception :
                print("디시콘이 없습니다.")
                exit()
            dccon_idx = 0
            unused_variable = os.system("clear")
            for dccon in dccon_list :
                dccon_title = dccon.find_element_by_class_name("dcon_name").get_attribute("innerHTML")
                print(str(dccon_idx) + " " + dccon_title)
                dccon_idx = dccon_idx+1

            print("Page Index : " + str(page_idx))
            print("원하는 인덱스의 번호를 입력하세요.")
            print("이전 페이지를 탐색하려면 P을 입력하세요.")
            print("다음 페이지를 탐색하려면 N을 입력하세요.")
            print("종료하시려면 X를 입력하세요")

            user_choice = input("입력 : ")
            if str(user_choice).isdigit() :
                #check user selection is bigger than list size
                if int(user_choice) > len(dccon_list) :
                    continue
                #user selected dccon
                #so parse it
                print(dccon_list[int(user_choice)].get_attribute("href"))
                driver.get(dccon_list[int(user_choice)].get_attribute("href"))

                print("check")

                #for correct page loading
                driver.refresh()
                driver.implicitly_wait(3)

                print("refresh")

                #wait 3 sec for load(server problems)
                imgSets = driver.find_elements_by_class_name("img_dccon")
                title = driver.find_element_by_class_name("font_blue").get_attribute('innerText')
                index = 0
                folder = ""

                #create folder
                if not os.path.exists(title) :
                    folder = title
                    os.makedirs(title)
                else :
                    folder = title+str(random.randrange(0,100))
                    os.makedirs(folder)

                for span in imgSets :
                    try :
                        img = span.find_element_by_tag_name("img")
                        src = str(img.get_attribute("src")).replace('dcimg5','image')
                        img_file = urllib.request.urlopen(src)
                        f = open("./"+folder+"/"+str(index)+".jpg",'wb')
                        f.write(img_file.read())
                        f.close()
                    except StaleElementReferenceException:
                        print("caused error")
                    finally :
                        index = index +1
                print("완료")
                exit()
            else :
                #if user choose exit, then exit
                if user_choice == 'x' | user_choice == 'X' :
                    exit()
                
                #user selected search next page.
                #there are three number of cases:
                #first, there are no more page(reached end of pages)
                #second, more page available
                #third, no pages in there (only 1 page)
                #so, first we should check we can go to next page
                #paging_box = driver.find_element_by_class_name("bottom_paging_box")
                #check a tag is available
                #current_page = paging_box.find_element_by_tag_name("em").get_attribute("innerHTML")
                #page_list = paging_box.find_elements_by_tag_name("a")
                #check more than 10 pages using "다음" button
                #next_button = None
                #try :
                #    next_button = driver.find_element_by_class_name("page_next")
                #except Exception as e:
                #    print(e)

                #if size is 0, no pages in there
                #if size is bigger than 1, check more page is available
