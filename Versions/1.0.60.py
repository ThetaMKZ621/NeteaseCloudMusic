#NeteaseCloudmusicDownloader
#version 1.0.60
#Python 3.9.6 on Windows 10 21H1
#Edited with VS Code
#Code by ThetaRain
#Updated July 30,2021

#Import Modules
import re
import os
import datetime



#Check whether the non-preinstall module "selenium", "requests" and "tqdm" has benn installed.
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print(r'Module "selenium" have not been installed!')
    print(r'Installing selenium...')
    i = os.system('pip install selenium')
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
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
    filename = filename + '.mp3'
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
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(url,stream = True,headers=headers)
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

#Function get_playlist()
#To get urls of songs in the playlist. Then put them in a list.
def get_playlist(options):
    print('HomePage of NeteaseCloudMusic will be open.')
    print('Open the playlist you want to download in the broswer.')
    print('--->We strongly recommand that you sign in before open the playlist.','\n')
    print('After opening the playlist, go back to this window.')
    i = input('Press [Enter] to open the browser.')
    browser = webdriver.Chrome(options=options)
    browser.get('https://music.163.com')
    print('Attention: Make sure you have just open one tab in the browser before you press [Enter]')
    i = input('If you have already opened the playlist, press [Enter]')
    print('Start to extract playlist')
    playlist = []
    browser.switch_to.frame('g_iframe')
    for links in browser.find_elements_by_xpath('//*[@class="txt"]/a'):
        href = links.get_attribute('href')
        playlist.append(href)
    print('Copmlete!')
    browser.quit()
    return playlist

i = os.system('cls')
print('NeteaseCloudmusicDownloader v1.0.60')
#Get work mode
print(
    '''\
        Choose work mode:
        1  ------  Single Url
        (Input a url and just download one song.)
        2  ------  Playlist
        (A broswer will be open and you can open your playlist and download it.)
        3  ------  List File
        (Downloader will read list.txt and download urls in it)
    '''
)
work_mode = int(input())

i = os.system('cls')

#Create new folder for this task.
new_folder =datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d-%H%M%S')
i = os.mkdir(os.path.dirname(__file__) + '\\' + new_folder)
download_path = os.path.dirname(__file__) + '\\' + new_folder + '\\'

#Settings for webdriver.Chrome()
options = Options()
#Disable logging
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#Do the corresponding things according to the work mode.
if work_mode == 1:
    print('Input url:','\n','(The Urls Looks Like: https://music.163.com/song?id=<SongID>)')
    url = input(">")
    i = os.system('cls')
    browser = webdriver.Chrome(options=options)
    print("If the page has been loaded for too long, please stop loading manually.")
    filename = list_to_name((get_info(url,browser)))
    id = url_to_id(url)
    message = download(id,download_path,filename)


if work_mode == 2 or work_mode == 3:
    if work_mode == 2:
        url_songlist = get_playlist(options)

    if work_mode == 3:
        print('Before you press [Enter], check whether list.txt exists')
        print('If not, creat one in %s' % os.path.dirname(__file__))
        print('Then edit list.txt and fill in the urls, a url each line.')
        print('(The Urls Looks Like: https://music.163.com/song?id=<SongID>)')
        print('If you have done, press [Enter]')
        i = input()
        i = os.system('cls')
        with open(os.path.dirname(__file__) + '\list.txt','r',encoding='utf-8') as file:
            url_songlist = file.read().splitlines()

    browser = webdriver.Chrome(options=options)
    print("If the page has been loaded for too long, please stop loading manually.")
    filenames = []
    ids = []
    for playlist in url_songlist:
        info = get_info(playlist,browser)
        filename_each = list_to_name(info)
        filenames.append(filename_each)
        id_each = url_to_id(playlist)
        ids.append(id_each)
    for x,y in zip(ids,filenames):
        print("Sone: ",y)
        message = download(x,download_path,y)
        print(message)

browser.quit()
print('\n')
print("All Requests Cleared.")

i = input('Press [Enter] to exit.')

        
