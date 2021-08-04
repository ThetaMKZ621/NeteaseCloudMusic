#NeteaseCloudmusicDownloader
#version 1.0.65
#Python 3.9.6 on Windows 10 21H1
#Edited with VS Code
#Code by ThetaRain
#Updated August 4,2021

#导入模块
import re
import os
import datetime



#检查第三方库 selenium, requests 和 tqdm 是否已经安装.
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print(r'模块 "selenium" 尚未被安装！')
    print(r'正在安装 selenium...')
    i = os.system('pip install selenium')
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
try:
    import requests
except ImportError:
    print(r'模块 "requests" 尚未被安装！')
    print(r'正在安装 requests...')
    i = os.system('pip install requests')
    import requests
try:
    from tqdm import tqdm
except ImportError:
    print(r'模块 "tqdm" 尚未被安装！')
    print(r'正在安装 tqdm...')
    i = os.system('pip install tqdm')
    from tqdm import tqdm


#函数 get_info()
#从网易云音乐的网页中获取歌曲信息，并导出至列表中
def get_info(url,browser):
    #使用 selenium 的 webdriver 功能唤出浏览器
    #注:"music.163.com"中歌曲信息部分作为框架嵌入主网页中，需要调用 "switch_to.frame" 方法来将爬虫指向框架
    browser.get(url)
    browser.switch_to.frame('g_iframe')
    info = []
    #在框架中爬取歌曲信息
    for _artist in browser.find_elements_by_css_selector('a[class="s-fc7"][href^=\/artist]'):
        info.append(_artist.text)
    for title in browser.find_elements_by_css_selector('em[class="f-ff2"]'):
        pass
    info.append(title.text)
    return info

#函数 list_to_name()
#将存有歌曲信息的列表转换为最终的文件名，命名规则与官方相同
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

#函数 url_to_id()
#导出歌曲ID，歌曲ID将会用于下载歌曲
def url_to_id(url):
    pattern = re.compile(r'\d+$')
    id = pattern.search(url).group()
    return id

#函数 download()
#用于下载歌曲
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
        #获取文件大小
        content_size = int(response.headers['content-length'])
        print("文件大小: "+str(round(float(content_size/1048576),1))+"[MB]")
        #使用 tqdm 来生成进度条，一般来说下载不会花很长时间（指进度条的意义不大）
        with open(path + name,'wb') as file:
            with tqdm(unit='B',unit_scale=True,unit_divisor=1024,leave=True,mininterval=0.25,maxinterval=2,miniters=1,total=int(content_size)) as bar:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    bar.update(chunk_size)
        message = "成功！"
    except Exception:
        message = "失败！"
    return message

#函数 get_playlist()
#抓取歌单中的歌曲链接，并导出至列表中
def get_playlist(options):
    print('网易云音乐的首页将会被打开')
    print('然后，在弹出的浏览器中打开要下载的歌单')
    print('--->强烈建议您在打开歌单前先登录，否则可能不能获取完整歌单','\n')
    print('打开歌单并加载完成之后，请回到这个窗口')
    i = input('按下 [Enter] 键打开浏览器.')
    browser = webdriver.Chrome(options=options)
    browser.get('https://music.163.com')
    print('注意：在进行下一步之前，确保您在弹出的浏览器中仅打开了一个标签页')
    i = input('如果您已经打开了歌单，请按下 [Enter] 键')
    print('开始获取歌单')
    playlist = []
    browser.switch_to.frame('g_iframe')
    for links in browser.find_elements_by_xpath('//*[@class="txt"]/a'):
        href = links.get_attribute('href')
        playlist.append(href)
    print('完成！')
    browser.quit()
    return playlist

i = os.system('cls')
print('NeteaseCloudMusicDownloader v1.0.65')
print('网易云音乐下载器 版本 1.0.65')
#获取工作模式
print(
    '''\
        选择工作模式:
        1  ------  单URL下载
        (仅下载一首歌曲)
        2  ------  歌单下载
        (一个浏览器将会打开，您可以在里面打开您的歌单并下载)
        3  ------  从 list.txt 下载
        (下载器将会读取存放于 list.txt 中的URL并下载)
    '''
)
work_mode = int(input())

i = os.system('cls')

#为这次下载任务创建新文件夹
new_folder =datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d-%H%M%S')
i = os.mkdir(os.path.dirname(__file__) + '\\' + new_folder)
download_path = os.path.dirname(__file__) + '\\' + new_folder + '\\'

#webdriver.Chrome() 的参数
options = Options()
#禁用日志输出
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#根据选定的工作模式执行不同的分支
if work_mode == 1:
    print('输入URL:','\n','(URL格式: https://music.163.com/song?id=<歌曲ID>)')
    url = input(">")
    i = os.system('cls')
    browser = webdriver.Chrome(options=options)
    print('如果页面长时间未加载完成（浏览器的加载动画未停止）请手动停止加载')
    filename = list_to_name((get_info(url,browser)))
    id = url_to_id(url)
    message = download(id,download_path,filename)


if work_mode == 2 or work_mode == 3:
    if work_mode == 2:
        url_songlist = get_playlist(options)

    if work_mode == 3:
        print('在进行下一步前检查 list.txt 是否已经存在')
        print('如果文件不存在，请在以下路径创建 list.txt： %s' % os.path.dirname(__file__))
        print('您现在可以编辑 list.txt 确保每行一个URL')
        print('(URL格式： https://music.163.com/song?id=<歌曲ID>)')
        print('准备就绪后，按下 [Enter] 键')
        i = input()
        i = os.system('cls')
        with open(os.path.dirname(__file__) + '\list.txt','r',encoding='utf-8') as file:
            url_songlist = file.read().splitlines()

    browser = webdriver.Chrome(options=options)
    print('如果页面长时间未加载完成（浏览器的加载动画未停止）请手动停止加载')
    filenames = []
    ids = []
    for playlist in url_songlist:
        info = get_info(playlist,browser)
        filename_each = list_to_name(info)
        filenames.append(filename_each)
        id_each = url_to_id(playlist)
        ids.append(id_each)
    for x,y in zip(ids,filenames):
        print("歌曲: ",y)
        message = download(x,download_path,y)
        print(message)

browser.quit()
print('\n')
print("任务完成！")

i = input('按下 [Enter] 键退出程序')       