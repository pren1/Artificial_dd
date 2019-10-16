# Artificial_dd

[![Generic badge](https://img.shields.io/badge/Tensorflow-keras-<COLOR>.svg)](https://shields.io/) 
[![Generic badge](https://img.shields.io/badge/github-dd_center-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Beam-search-<COLOR>.svg)](https://shields.io/)
<p>
    <img src="model_picture/dd_center.png"/>
</p>

### ⚠️ Notification

Please keep this repo **private**, and please notice that this is **not** an open-source software currently. 

### 🌲 Request Packages

[![Generic badge](https://img.shields.io/badge/gdown-orange.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/keras-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/numpy-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/scipy-blueviolet.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/tqdm-lightgrey.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/jieba-ff69b4.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/flask-success.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/uwsgi-yellow.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/pandas-grey.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/pydot-cyan.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/graphviz-brown.svg)](https://shields.io/)

### 📃 Introduction

A software that can send context-based fake danmaku. 

Please write more things here if any of you want to describe this project...

### 🎉 Demo

We got a [demo video](https://pan.baidu.com/s/18Pkr_VAEnXuME-NMG7HMdQ) here! Yeah!

### ☁️ Model structure

This is a sequence-to-sequence model with the attention mechanism. The encoder is used to compress the information in input messages, and the decoder is responsible for generating new texts based on the inputs. Here is the model structure:

<p>
    <img src="model_picture/model.png"/>
</p>

### ⚡️ Quick start

1. Run the following command, and you should see two folders named 'content' and 'tmp'.
```
bash ./download_sources.sh
```
2. Then, run:
```
uwsgi --http :8001 --enable-threads --wsgi-file ./model_process.py --callable app
```
3. After that, you should figure out your room id. Here are some frequently used examples. Note that not all the vtubers are tested, so use this model at your own risk.
```json
{
    "1": "猫宫日向Official",
    "16": "新科娘Official",
    "38": "大神澪Official",
    "54": "AIChannel官方",
    "70": "白上吹雪Official",
    "96": "紫咲诗音Official",
    "133": "輝夜月Official",
    "146": "神子杏-Official",
    "152": "兔纱mimi_Official",
    "191": "神楽七奈Official",
    "224": "陆婉莹GodRiku",
    "233": "湊-阿库娅Official",
    "258": "未来明-MiraiAkari",
    "266": "夏色祭Official",
    "283": "茯苓猫不黑",
    "286": "神楽Mea_Official",
    "309": "犬山玉姬Official",
    "322": "泠鸢yousa"
}
```
Take a look at the room_id_mapping.json under the content folder for other vtubers.

4. After that, post a message to Server_ip:8001 in the following format. You should also specify the room_id this time, and it will boost the performance:
```json
{
    "message":"kuso和夏哥撞车了, 2333333333, 哈哈哈哈哈哈, 哈哈哈哈哈哈哈哈哈哈哈", 
    "room_id": 266
}
```
The python program should respond:
```json
{
    "result": "not enough input messages"
}
```
However, if you send enough inputs, the program will return the generated messages:
```json
{
    "result": [
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "上手上手\n",
        "夏哥赶紧上舰（自闭）\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "草\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "似曾相识\n",
        "草\n",
        "草\n",
        "23333\n",
        "我同意哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "左边说马自立想吃舰长是个屑\n",
        "唉，我要看转播的梗\n",
        "夏哥，fbk吃番茄！\n",
        "马自立是我老婆！\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "夏哥吃！(哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "我全都要\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "草\n",
        "草\n",
        "草\n",
        "草\n",
        "草\n",
        "草\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "草\n",
        "草\n",
        "斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯哈斯",
        "舰长上舰！！！！\n",
        "说的好 你别地形啊（意味深）\n",
        "草\n",
        "全是老父亲啊\n",
        "我以为是哪迫害马自立 哈哈\n"
    ]
}
```
