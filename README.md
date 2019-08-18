# Artificial_dd
Please keep this repo **private**, and this is not an open-source software currently.

### 1. Introduction
A software that can send context-based fake danmaku
Please write more things here if any of you want to describe this project...

### 2. Model structure
This is a sequence-to-sequence model with attention mechanism utilized. The encoder is used to compress the information in input messages, and the decoder is responsible for generating new texts based on the inputs. Here is the model structure:

<p>
    <img src="model_picture/model.png"/>
</p>

### 3. Utilization
1. Run the following command, and you should see two folders named 'content' and 'tmp'.
```
bash ./download_sources.sh
```
2. Run the following command, and you should see the outputs.
```
python3 model_process.py
```
