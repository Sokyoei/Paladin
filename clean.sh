#!/bin/bash

rm -rf ./dist
find . -name *.so | xargs rm -f
