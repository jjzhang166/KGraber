# KGraber

**这是一个用来从网页版全民K歌抓取用户自己作品并下载到本地的脚本**

---
Author: wangzhizhou(Joker)

Email: 824219521@qq.com

---

# Python 方式
    
    如果你对python比较熟悉，可以`clone`源码后，使用可编辑源码的方式安装该包，如下命令

```
$ pip install -e .
```

## 使用

```
$ KGraber
```

- 要使用`全民K歌`手机App内置的二维码扫码功能

- 脚本创建名为`songs`的目录保存已下载的用户歌曲


# 下载预编译二进制运行

下载对应平台的可执行文件后，在Mac/Linux下需要给文件开启执行权限： `$ sudo chmod u+x KGraber`后，再在终端中运行。在Windows下可以直接点击`.exe`文件执行。

## 下载

- [mac_x64](https://github.com/wangzhizhou/KGraber/raw/master/release/mac_x64/KGraber)

- [windows_x64](https://github.com/wangzhizhou/KGraber/raw/master/release/windows_x64/KGraber.exe)

# 在具体平台上编译二进制的方法

### 安装相关包

```
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ pip install -e .
```

### Mac平台

```
$ pyinstaller --clean -F --workpath release --specpath release --distpath release/mac_x64 -n KGraber release.py
```

### Windows 平台

```
$ pyinstaller --clean -F --workpath release --specpath release --distpath release/windows_x64 -n KGraber.exe release.py
```

# 本包已提交到PyPi Index上，所以也可以使用下面方法安装

```
$ pip install KGraber
```
**Enjoy It**


pipa: `d2FuZ3poaXpob3UrV3c1NDM4NTkyMzAK`