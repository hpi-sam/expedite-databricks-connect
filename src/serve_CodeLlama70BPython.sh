#!/bin/bash

# Run with "bash serve_CodeLlama70BPython.sh"
CUDA_VISIBLE_DEVICES=0,1,2,3;
vllm serve meta-llama/CodeLlama-70b-Python-hf --trust-remote-code --max-model-len 4096 --tensor-parallel-size 4 --api-key token-abc123
