# 网易云音乐下载器  
# NeteaseCloudMusicDownloader  
一个简单的下载器，可以下载网易云音乐中的歌曲。  
以 _selenium WebDriver_ 实现爬虫抓取功能。  
了解[selenium](https://selenium.dev/)  
A simple downloader which is able to download music from NeteaseCloudMusic.  
Using _selenium WebDriver_ to realize Web Crawler Function.  
About [selenium](https://selenium.dev/)  
- - -
## 使用环境要求/REQUIREMENTS  
### Python 3.4 或更高版本/Python 3.4 or higher version  
### 系统中装有网络浏览器（现版本仅支持Chrome）/Web browser(But now support Chrome only.)  
### 浏览器驱动程序/Web Drivers  
#### 你可以从以下网站下载对应的浏览器驱动程序/You can download it from following sites:  
>[Chrome/Chromium](https://sites.google.com/chromium.org/driver/)  
>[Firefox](https://github.com/mozilla/geckodriver/)  
>[Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)  
>[Opera](https://github.com/operasoftware/operachromiumdriver/)  
>[Safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)  
- - -
## 如何使用/How to use?  
首先，确保浏览器驱动程序（对Chrome来说，这个驱动程序的名称是 _chromedriver.exe_）已经在下载器程序文件的根目录下  
First, make sure the webdriver programme(For Chrome, it's _chromedriver.exe_) and _Downloader.py_ are in the same directory.  
  
然后，运行 _Downloader.py_ 并根据提示操作  
Then，run _Downloader.py_ and follow the prompts.  
  
歌曲将会被下载到一个以当前日期和时间命名的文件夹  
The downloaded songs will be in a newly created floder that named after the current date and time.  


这个项目仍在开发中，后续版本将加入更多功能，敬请期待  
This project is still developing. More function will be added in subsequent versions.  
- - -
## 改进目标/Goals  
- [x] 解决页面加载超时需要手动停止加载的问题/Fix timeouts problem which needs to stop loading manually.
- [x] 在获取歌曲信息部分改用无界面模式/Make Headless Mode available in the process of fetching info of songs.
- [x] 引入可修改的配置文件以实现部分自定义项/Make custom-edited configuring available.
- [x] 加入下载日志功能/Add logging function.
- [ ] 加入异常处理功能/Add Error Handlers.
> 适配其他浏览器/Add supports for other browsers.  
> - [ ] Firefox
> - [ ] Edge
> - [ ] Opera
> - [ ] Safari
