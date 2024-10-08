#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=../../proto/statistics --pyi_out=../../proto/statistics --grpc_python_out=../../proto/statistics protocols_statistics.proto
