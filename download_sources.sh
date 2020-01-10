#!/usr/bin/env bash
# Download everything you need

gdown https://drive.google.com/uc?id=1OLGdD_oLaqMCsvTc-o3kO48YLD3zgo8c
gdown https://drive.google.com/uc?id=1IGYFwHnEvAg9y5_bkkxRGTNUYhSN7ZYm
gdown https://drive.google.com/uc?id=1P6czaa39VYBtHTe_B8YbHK7e_zd617Jw
gdown https://drive.google.com/uc?id=1z1q56jYC0YDDjZVHBBAKnx4CyAUL-L3t
gdown https://drive.google.com/uc?id=1sqah0x_1SoPG5kk11OSyxDkD5mfT41bJ



mkdir content
mkdir tmp
# Move to target folder
mv glove-512-words.pkl ./content/
mv glove-512.npy ./content/
mv room_id_mapping.json ./content/

mv encoder.h5 ./tmp/
mv decoder.h5 ./tmp/