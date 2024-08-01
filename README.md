# PJDL_mcz2tres

## 这是一个过时版本，请查看(https://github.com/suizhuchen/malody2PJDL)[https://github.com/suizhuchen/malody2PJDL]

基于python实现mcz谱面文件解压缩并转换为Project DaoLi谱面文件的程序

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

---

## 目录

- [总述](#总述)
- [如何使用](#如何使用)

### 总述

首先，就目前版本而言，你需要解包PJDL，这是一种不道德的行为，不推荐，不提倡逆向游戏。

**本文不会讲述任何关于逆向PJDL的内容**

### 如何使用

1. 逆向PJDL
2. 将本项目clone到本地

```sh
git clone https://github.com/suizhuchen/PJDL_mcz2tres.git
```

3. 在你的Python环境中安装pillow库

```sh
pip install pillow
```

4. 运行main.py，将要转换的mcz文件放在py文件目录下，输入mcz文件名（包含后缀）。之后在列表里选择要转换的文件序号。
5. 若运行无误，则可在py文件目录下找到对应mcz文件名的文件夹，其中export目录下便是转换后的谱面文件。
6. 在PJDL项目文件夹下，将谱面，音乐，曲绘放在正确位置，在Godot里，找到menu场景，添加谱面文件
7. 现在您可以测试转换结果了

<!-- links -->


[contributors-shield]: https://img.shields.io/github/contributors/suizhuchen/PJDL_mcz2tres.svg?style=flat-square

[contributors-url]: https://github.com/suizhuchen/PJDL_mcz2tres/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/suizhuchen/PJDL_mcz2tres?style=flat-square

[forks-url]: https://github.com/suizhuchen/PJDL_mcz2tres/network/members

[stars-shield]: https://img.shields.io/github/stars/suizhuchen/PJDL_mcz2tres?style=flat-square

[stars-url]: https://github.com/suizhuchen/PJDL_mcz2tres/stargazers

[issues-shield]: https://img.shields.io/github/issues/suizhuchen/PJDL_mcz2tres.svg?style=flat-square

[issues-url]: https://img.shields.io/github/issues/suizhuchen/PJDL_mcz2tres.svg

[license-shield]: https://img.shields.io/github/license/suizhuchen/PJDL_mcz2tres.svg?style=flat-square

[license-url]: https://github.com/suizhuchen/PJDL_mcz2tres/blob/master/LICENSE.txt




