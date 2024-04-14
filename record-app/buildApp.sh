#!/bin/bash

cd android
./gradlew assembleRelease

cp app/build/outputs/apk/release/app-release.apk ../record-app.apk