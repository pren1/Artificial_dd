# Artificial_dd
Please keep this repo **private**, this is not an open source software currently.
A software that can send context-based fake danmaku

### 1. Introduction
Whoever want to describe this project please write something here...

### 2. Model structure
This is a seqence-to-sequence model with attention mechanism utilized. The encoder is used to compress the information in input messages, and the decoder is responsible for generating new texts based on the inputs. Here are the model structure:





### 3. Utilization
1. Run the following command, you should see two folders named 'content' and 'tmp'.
```
bash ./download_sources.sh
```
2. Run the following command, you should see the outputs.
```
python3 model_process.py
```
