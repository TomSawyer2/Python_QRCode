# Python_QRCode WebUI

## 简介

Python_QRCode WebUI 是一个基于 Python_QRCode 的 WebUI，可以在网页中进行二维码的编码/解码。

## 开发

```bash
npm config set registry https://registry.npmmirror.com
npm i pnpm -g
pnpm i 
pnpm run dev
```

## 部署

```bash
pnpm run build
```

**在外部的`web.py`启动Flask服务后会自动代理`/dist`中的内容，因此不需要安装相关依赖，不忽略`/dist`的内容。**
