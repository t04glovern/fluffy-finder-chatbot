#!/bin/bash

cd "$(dirname "$0")"
rm builds/lambda-build.zip
cd lambda
mkdir build
pip3 install requests -t build
cp * build
zip -r ../builds/lambda-build.zip build
rm -rf build
