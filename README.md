# Python_QRCode

## 简介

Python实现的二维码编解码功能 [TomSawyer2@GitHub](https://github.com/TomSawyer2)

## 使用

### Pre

```bash
pip install -r requirements.txt
```

### 一、命令行模式

#### 编码

```bash
python main.py --encode --data="Hello World"
python main.py --encode -d "Hello World!" -o file --outputdir=./ -f "HelloWorld.png"
python main.py --encode -d README.md -o file --outputdir=./ -f "README.png" -t file
python main.py --encode -d .gitignore -o file --outputdir=./ -f "gitignore.png" -t file --backcolor=white --fillcolor="#66ccff"
```

参数说明（加粗代表必须有）：
**`-d/--data`**: 需要编码的数据，可以是字符串，也可以是文件路径
`-t/--type`: 输入的类型，`text`或`file`，默认为字符串
`-o/--output`: 二维码输出类型，`file`或`terminal`，默认为终端输出
`--outputdir`: 输出文件夹，格式为`./path/to/dir/`，默认为`./qrcode/assets/`
`-f/--filename`: 输出文件名，包含后缀，默认为`output-当前时间戳.png`
`--backcolor`: 背景色，可以是颜色英语，也可以是十六进制数据，默认为白色
`--fillcolor`: 填充色，可以是颜色英语，也可以是十六进制数据，默认为黑色

#### 解码

```bash
python main.py --decode --data="qrcode/assets/githubQRCode.png"
python main.py --decode --data="README.png"
python main.py --decode --data="qrcode/assets/githubQRCode.png, https://cdn.tomsawyer2.xyz/pics/githubQRCode.png"
```

参数说明（加粗代表必须有）：
**`--data`**: 需要解码的数据，可以是网络上图片的URL，也可以是文件路径

支持同时解码多个二维码，只需要在`--data`后面加上英文逗号，然后输入多个二维码的路径或URL即可
**注意：同时解码多个二维码时文件路径、URL中不能包含英文逗号，否则会出错**

### 二、WebUI模式

```bash
python main.py --web
```

浏览器中打开127.0.0.1:5000

### 三、插件模式

直接作为python库引入使用

## todo

### 二维码编码

- [x] 通过命令行参数传入
- [x] 通过本地文件解析
- [x] 通过命令行图案输出
- [x] 通过图片文件输出
- [x] 大数据量编码

### 二维码解码

- [x] 通过本地图片文件解析
- [x] 通过网络图片的URL解析
- [x] 批量解码
- [x] 依赖替换

### 杂项

- [x] WebUI
- [x] 集成函数
- [ ] 单元测试
- [ ] 编码文档
- [x] 本地依赖检测脚本
