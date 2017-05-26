#!/bin/bash

fname=`basename $1`
curl -O $1

echo "downloaded $fname"
unzip $fname
