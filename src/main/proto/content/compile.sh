#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=../../proto/content --pyi_out=../../proto/content --grpc_python_out=../../proto/content protocols_content.proto
