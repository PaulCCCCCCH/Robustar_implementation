#!/bin/bash

function getTorchCPU {
    python3.9 -m pip install \
    torch==2.2.0 \
    torchvision==0.17.0 \
    torchattacks==3.4.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cpu
}

function getTorchCUDA117 {
    python3.9 -m pip install \
    torch==2.0.1 \
    torchvision==0.15.2 \
    torchattacks==3.4.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu117
}

function getTorchCUDA118 {
    pip install \
    torch==2.2.0 \
    torchvision==0.17.0  \
    torchattacks==3.4.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu118
}

function getTorchCUDA121 {
    pip install \
    torch==2.2.0 \
    torchvision==0.17.0  \
    torchattacks==3.4.0 \
    pytorch_influence_functions==0.1.1 \
    flashtorch==0.1.3 \
    -f https://download.pytorch.org/whl/cu121
}

function installPyTorch {
    if [ "$1" == "cpu" ]; then
        getTorchCPU
    elif [ "$1" == '11.7' ]; then
        getTorchCUDA117
    elif [ "$1" == '11.8' ]; then
        getTorchCUDA118
    elif [ "$1" == '12.1' ]; then
        getTorchCUDA121
    else
        echo "CUDA version $1 not supported."
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