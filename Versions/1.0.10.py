#NeteaseCloudmusicDownloader
#version 1.0.10 beta
#Python 3.9.6 on Windows 10 21H1
#Edited with VS Code
#Code by ThetaRain
#Updated July 29,2020

#Import Modules
import re
import os
import datetime

#Check whether the non-preinstall module "selenium", "requests" and "tqdm" has benn installed.
try:
    from selenium import webdriver
except ImportError:
    print(r'Module "selenium" have not been installed!')
    print(r'Installing selenium...')
    i = os.system('pip install selenium')
    from selenium import webdriver
try:
    import requests
except ImportError:
    print(r'Module "requests" have not been installed!')
    print(r'Installing requests...')
    i = os.system('pip install requests')
    import requests
try:
    from tqdm import tqdm
except ImportError:
    print(r'Module "tqdm" have not been installed!')
    print(r'Installing tqdm...')
    i = os.system('pip install tqdm')
    from tqdm import tqdm

i = os.system('cls')

#Function get_info()
#To extract information of songs from Netease's web page, then put it into a list.
def get_info(url,browser):
    #Using webdriver of selenium to simulate browser to access web pages.
    #Attention:"music.163.com" puts songs' info in a frame, so next it has to "switch_to.frame" first.
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    info = []
    #Searching songs' info in the frame.
    for _artist in browser.find_elements_by_css_selector('a[class="s-fc7"][href^=\/artist]'):
        info.append(_artist.text)
    for title in browser.find_elements_by_css_selector('em[class="f-ff2"]'):
        pass
    info.append(title.text)
    return info

#Function list_to_name()
#To convert the information of songs to formatted filename, just like the songs you download from the Cloudmusic App.
def list_to_name(list):
    filename = ""
    number = 0
    for n in list:
        if number == 0:
            filename = filename + n
            number += 1
        elif number == len(list) - 1:
            filename = filename + ' - ' + n
        else:
            filename = filename + ',' + n
            number += 1
    return filename

#Function url_to_id()
#To extract id of the song. It will be needed in the downloading process.
def url_to_id(url):
    pattern = re.compile(r'\d+$')
    id = pattern.search(url).group()
    return id

#Function download()
#For download, that's all.
def download(id,path,name):
    try:
        url = 'http://music.163.com/song/media/outer/url?id=' + id + '.mp3'
        response = requests.get(url,stream = True)
        chunk_size = 1024
        #Get the size of the file.
        content_size = int(response.headers['content-length'])
        print("Size: "+str(round(float(content_size/1048576),1))+"[MB]")
        #Use "tqdm" to create a progress bar.But for the most time, downloading won't spend much time.
        with open(path + name,'wb') as file:
            with tqdm(unit='B',unit_scale=True,unit_divisor=1024,leave=True,mininterval=0.25,maxinterval=2,miniters=1,total=int(content_size)) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    bar.update(chunk_size)
        message = "Success!"
    except Exception:
        message = "Fail!"
    return message

#Create new folder for this task.
new_folder =datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d-%H%M%S')
i = os.mkdir(os.path.dirname(__file__) + '\\' + new_folder)
download_path = os.path.dirname(__file__) + '\\' + new_folder + '\\'

#Open the broser. In this sample, I choose Google Chrome as its browser.
browser = webdriver.Chrome()
#Read urls from "list.txt".
with open(os.path.dirname(__file__) + '\list.txt','r',encoding='utf-8') as file:
    list = file.read().splitlines()

for url in list:
    x = get_info(url,browser)
    filename = (list_to_name(x) + '.mp3')
    id = url_to_id(url)
    message = download(id,download_path,filename)
    print(message + '\n')

print("All Requests Cleared.")
browser.quit()
