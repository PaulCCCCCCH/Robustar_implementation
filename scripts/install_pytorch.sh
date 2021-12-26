#!/bin/bash

function getTorchCPU {
    python3.7 -m pip install \
    torch==1.9.1 \
    torchvision==0.10.1 \
    torchattacks==3.1.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html
}

function getTorchCUDA92 {
    pip install \
    torch==1.7.0+cu92 \
    torchvision==0.8.0+cu92 \
    torchattacks==3.1.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu92/torch_stable.html 
}

function getTorchCUDA102 {
    pip install \
    torch==1.9.1+cu102 \
    torchvision==0.10.1+cu102  \
    torchattacks==3.1.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu102/torch_stable.html 
}

function getTorchCUDA111 {
    pip install \
    torch==1.9.1+cu111 \
    torchvision==0.10.1+cu111  \
    torchattacks==3.1.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu111/torch_stable.html 
}

function getTorchCUDA113 {
    pip install \
    torch==1.9.1+cu113 \
    torchvision==0.10.1+cu113  \
    torchattacks==3.1.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu113/torch_stable.html 
}

function installPyTorch {
    if [ "$1" == "cpu" ]; then
        getTorchCPU
    elif [ "$1" == '9.2' ]; then
        getTorchCUDA92
    elif [ "$1" == '10.2' ]; then
        getTorchCUDA102
    elif [ "$1" == '11.1' ]; then
        getTorchCUDA111
    elif [ "$1" == '11.3' ]; then
        getTorchCUDA113
    else
        echo "CUDA version not supported."
        exit 1
    fi
}

while getopts c: FLAG 
do
    case "$FLAG" in 
        c) VCUDA=${OPTARG};;
    esac
done
installPyTorch "$VCUDA"