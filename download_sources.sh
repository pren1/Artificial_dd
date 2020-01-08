#!/usr/bin/env bash
# Download everything you need

#https://drive.google.com/file/d/1seNCUJYzxFTt5GUmNyzJBvs8EnC03k1u/view?usp=sharing
#https://drive.google.com/file/d/1YcRTM5wX6kkK1S4cMl4Bb7L9bfn7jwWY/view?usp=sharing
#https://drive.google.com/file/d/1UHAUWW-et7dm3yxPL-D6zjEc4g-MTU97/view?usp=sharing
#https://drive.google.com/file/d/1_R_FiqrlVdZlN2Fy8xHx2bwq9ZYyu31o/view?usp=sharing
#https://drive.google.com/file/d/1YHHbnfIM3zdmc8EKmAbywhCjalHquNVB/view?usp=sharing

gdown https://drive.google.com/uc?id=1seNCUJYzxFTt5GUmNyzJBvs8EnC03k1u
gdown https://drive.google.com/uc?id=1YcRTM5wX6kkK1S4cMl4Bb7L9bfn7jwWY
gdown https://drive.google.com/uc?id=1UHAUWW-et7dm3yxPL-D6zjEc4g-MTU97
gdown https://drive.google.com/uc?id=1_R_FiqrlVdZlN2Fy8xHx2bwq9ZYyu31o
gdown https://drive.google.com/uc?id=1YHHbnfIM3zdmc8EKmAbywhCjalHquNVB

mkdir content
mkdir tmp
# Move to target folder
mv glove-512-words.pkl ./content/
mv glove-512.npy ./content/
mv room_id_mapping.json ./content/

mv encoder.h5 ./tmp/
mv decoder.h5 ./tmp/