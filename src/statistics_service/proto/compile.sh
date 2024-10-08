#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=../proto --pyi_out=../proto --grpc_python_out=../proto protocols.proto
