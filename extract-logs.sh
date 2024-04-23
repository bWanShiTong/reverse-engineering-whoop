#!/bin/bash

mkdir temp
cd temp
adb bugreport bugreport
unzip bugreport.zip


TIME=$(date +%Y-%m-%dT%H:%M:%S)

mv FS/data/log/bt/btsnoop_hci.log ../logs/${TIME}.log
mv FS/data/log/bt/btsnoop_hci.log.last ../logs/${TIME}.log.last

cd ..
rm -rf temp