#coding:utf-8
from setuptools import setup, find_packages

setup(
    name='KGraber',
    version=1.1,
    description=(
        '这是一个用来从网页版全民K歌抓取用户自己作品并下载到本地的脚本'
    ),
    long_description=open('README.md').read(),
    author='王志舟<wangzhizhou>',
    author_email='824219521@qq.com',
    maintainer='王志舟',
    maintainer_email='824219521@qq.com',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/wangzhizhou/KGraber',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    install_requires=[
        'beautifulsoup4',
        'requests',
        'qrcode',
        'pillow',
    ],
    entry_points = {
        'console_scripts': [
            'KGraber = KGraber:grabe'
        ]
    }
)