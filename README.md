# NeteaseCloudMusicDownloader
A simple downloader which is able to download music from NeteaseCloudMusic.  
Based on selenium Project.
## REQUIREMENTS
### Python 3.4 or higher version  
### A web broser(But now support Chrome only.)  
### Web Drivers  
#### You can download it from following sites:  
[Chrome/Chromium](https://sites.google.com/chromium.org/driver/)  
[Firefox](https://github.com/mozilla/geckodriver/)  
[Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)  
[Opera](https://github.com/operasoftware/operachromiumdriver/)  
[Safafi](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)  

## How to use?
Make sure the webdriver programme(For Chrome, it's _chromedriver.exe_) and _Downloader.py_ are in the same directory.  
Copy the urls of songs which you want to download to _list.txt_(It's in the same directory as _Downloader.py_).A url each line.  
_The url looks like this:_
```
https://music.163.com/song?id=1386838818
```
Run _Downloader.py_  
There will be a new floder named after the current date and time.The downloaded songs will be in that floder.  
That's all.  

This Downloader is still developing.More function will be added in subsequent versions.
