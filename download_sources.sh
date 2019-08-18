#!/usr/bin/env bash
# Download everything you need
gdown https://drive.google.com/uc?id=1V5juWnxQXwOOxJarxJ0V8-nVPF87QshX
gdown https://drive.google.com/uc?id=1B0UaIeixggEg30SUw3uvWxDGbabJo9NV
gdown https://drive.google.com/uc?id=1QLl2kqsPDoWhbmM22N9bdt1gOsuLRAdv
gdown https://drive.google.com/uc?id=11oycRZUgPN3eFgQy_ZvADUwv9IzUEt0g
gdown https://drive.google.com/uc?id=1wRVWnrJJPXz4E6I8x2sIoxlOFdWu1uMJ

mkdir content
mkdir tmp
# Move to target folder
mv glove-512-words.pkl ./content/
mv glove-512.npy ./content/
mv new_filtered_data.json ./content/

mv encoder.h5 ./tmp/
mv decoder.h5 ./tmp/