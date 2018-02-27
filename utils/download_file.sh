#!/bin/bash

fname=`basename $1`
curl -o data/$fname $1

echo "downloaded data/$fname"
unzip data/$fname
