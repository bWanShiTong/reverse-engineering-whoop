#!/bin/bash

rm -rf android

expo prebuild

cd android
./gradlew assembleRelease

cp app/build/outputs/apk/release/app-release.apk ../record-app.apk