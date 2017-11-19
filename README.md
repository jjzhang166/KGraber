# KGraber

**这是一个用来从网页版全民K歌抓取用户自己作品并下载到本地的脚本**

---
Author: wangzhizhou(Joker)

Email: 824219521@qq.com

---

## 安装

```
$ pip install -e .
```

## 使用

```
$ KGraber
```

- 要使用`全民K歌`手机App内置的二维码扫码功能

- 脚本创建名为`songs`的目录保存已下载的用户歌曲


## 编译的二进制 - 以mac上为例

```
$ pip install -r requirements.txt
$ pip install .
$ pyinstaller --clean -F --workpath release --specpath release --distpath release/mac_x64 -n KGraber release.py
```

## 下载

- [mac_x64](./release/mac_x64/KGraber)
- [windows_x64](./release/windows_x64/KGraber.exe)
- [linux_armv7](./release/linux_armv7/KGraber)

**Enjoy It**





