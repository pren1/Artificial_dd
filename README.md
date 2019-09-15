# Artificial_dd

[![Generic badge](https://img.shields.io/badge/Tensorflow-keras-<COLOR>.svg)](https://shields.io/) 
[![Generic badge](https://img.shields.io/badge/github-dd_center-<COLOR>.svg)](https://shields.io/)
<p>
    <img src="model_picture/dd_center.png"/>
</p>
### ⚠️ Notification

Please keep this repo **private**, and please notice that this is **not** an open-source software currently. 

### 📃 Introduction

A software that can send context-based fake danmaku. 

Please write more things here if any of you want to describe this project...

### ☁️ Model structure

This is a sequence-to-sequence model with an attention mechanism. The encoder is used to compress the information in input messages, and the decoder is responsible for generating new texts based on the inputs. Here is the model structure:

<p>
    <img src="model_picture/model.png"/>
</p>

### 🚧 Utilization

1. Run the following command, and you should see two folders named 'content' and 'tmp'.
```
bash ./download_sources.sh
```
2. Run the following command, and you should see the outputs.
```
python3 model_process.py
```

### 🎉 Output example

With inputs:
```
？？？
要让老师小心一点
太可爱了
前面的泥垢了
没有超美丽3d，白等了
？没见过这种包法呀
awsl
来了来了
封面为什么这么骚
同问
2333
三次元的朋友也不能放弃啊
awsl
awsl
awsl
```
Here are the outputs:
```
阿伟出来受死！
wwwww
wwwwwwwwwwwwwwwwwwwwww
可爱
awsl
awsl
awsl
草
awsl
awsl
爱酱好可爱
awsl
阿伟出来受死
awsl
awsl
awsl
114514
你不要过来啊
阿伟死了
```

### ⚡️ Quick start

First, create an instance and load the model. 

The program will be more time-consuming if you increase the parameter 'BATCH_SIZE', but you will get better results. So, there is a trade-off here. For instance, under current configuration, it took 6.7 seconds to generate 20 fake danmakus on my computer. We could expect it to be much faster in a GPU.

```python
from model_process import model_process
'Initialize'
mp = model_process(BATCH_SIZE = 500)
'Create a generator, load in the trained model'
mp.prepare_for_generator()
```

Second, get the input data.
```python
'We assume we have the following inputs'
data = input_data().return_example_input_list()
input_data().show_input_data()
```
At this step, you should see the following outputs in the console. That's what the program expects as inputs:
```
read in data:
>> 今晚我不睡了！
>> 刺激刺激
>> washoi
>> 马自立唱歌……
>> 爷不睡了
>> 夏哥播，我就陪夏哥熬
>> 夏哥深夜档
>> ｋｋｓｋ
>> 玩光明上下的先踢了
>> dd们换牌子
>> 半夜唱歌？
>> こんばんわっしゅい
>> washoi
>> washoi
>> (｀・ω・´)牙白
```

Then, whenever the new data is available, feed it into the feed_in_data function. Here we use a for loop to simulate this process:
```python
'Use a loop to iterate the data'
for single_data in data:
    'Every time there is a new message available, feed in the data'
    returned_result = mp.feed_in_data(single_data)
```
Whenever there is enough data, the model will output the fake danmakus to the 'returned_result', which is a list. Otherwise, the list will be empty.
