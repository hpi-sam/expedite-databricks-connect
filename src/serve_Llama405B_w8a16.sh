#!/bin/bash

# Run with "bash serve_Llama405B_w8a16.sh"
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7,8;
vllm serve neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w8a16 --trust-remote-code --max-model-len 8192 --tensor-parallel-size 8 --api-key token-abc123
