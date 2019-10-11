#!/usr/bin/env bash
# Download everything you need
#gdown https://drive.google.com/uc?id=1V5juWnxQXwOOxJarxJ0V8-nVPF87QshX
#gdown https://drive.google.com/uc?id=1B0UaIeixggEg30SUw3uvWxDGbabJo9NV
#gdown https://drive.google.com/uc?id=1QLl2kqsPDoWhbmM22N9bdt1gOsuLRAdv
#gdown https://drive.google.com/uc?id=11oycRZUgPN3eFgQy_ZvADUwv9IzUEt0g
#gdown https://drive.google.com/uc?id=1wRVWnrJJPXz4E6I8x2sIoxlOFdWu1uMJ

gdown https://drive.google.com/uc?id=1zEy1FI8IJJNPqbF_u4fw1LYb6LRJFcR8
gdown https://drive.google.com/uc?id=1BNho7u9E3bpRnIUrkJzyqFxHg1xgtFCW
gdown https://drive.google.com/uc?id=1FFSNsBeFlevU8v3xfQCUvDCBNSuP52PL
gdown https://drive.google.com/uc?id=1Hjwx_3CGCOUP3j8Uhae1y9aa0x7pj2Pg
gdown https://drive.google.com/uc?id=156SFMyNGyedud-6XJcYSnaYtXNkiAbVN

mkdir content
mkdir tmp
# Move to target folder
mv glove-512-words.pkl ./content/
mv glove-512.npy ./content/
mv room_id_mapping.json ./content/

mv encoder.h5 ./tmp/
mv decoder.h5 ./tmp/