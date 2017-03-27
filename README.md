# KGraber

**这是一个用来从网页版全民K歌抓取用户自己作品并下载到本地的脚本**

---
Author: wangzhizhou(Joker)
Email: 824219521@qq.com

---
- 运行脚本需要`python3`环境，并且有`pip`包管理器支持
- 需要安装`git`和`wget`下载工具
	- MacOS: brew install wget
	- Linux: sudo apt-get -y install wget

## 整个抓取过程有视频演示

### 下载KGraber工程到本地

- ![demo1.gif](./demos/demo1.gif)

```
git clone https://github.com/wangzhizhou/KGraber.git
```
### 登录全民K歌个人中心，获取全部音乐列表

- ![demo2.gif](./demos/demo2.gif)

### 以全部网页形式保存个人中心音乐列表网页到KGraber工程目录下

- ![demo3.gif](./demos/demo3.gif)

```
-_-# 这部分需要手动操作了，我功力还不能解决这部分自动化问题
```

###  运行脚本下载你的所有音乐到KGraber工程下的songs目录下面

- ![demo4](./demos/demo4.gif)

```
./dowload.sh
```

### 查看songs目录下下载的音乐的个数

- ![demo5.gif](./demos/demo5.gif)


## 注意


* 从网页上保存的htm文件命名为`personal.htm`，这是因为脚本中对文件的读取已经写死。如果你使用其它的浏览器，保存文件后名字为`personal.html`的，请把`html`修改为`htm`扩展名，便于自动运行脚本

* `install-deps.sh`脚本是用来安装python3用来解析`html`的库`BeautifulSoup4`

* `KGraber.py`的作用是从`personal.htm`中解析出用户音乐列表的下载地址和对应用的音乐名称，保存
	在`playlist.txt`文件中
	
* 最终`download.sh`会在内部调用上面所有的脚本，并创建一个名为`songs`的目录，并把用户的所有歌曲下载到该目录下面

**Enjoy It**





