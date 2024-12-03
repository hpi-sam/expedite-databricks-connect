#!/bin/bash

# Run with "bash serve_Llama405B.sh"
CUDA_VISIBLE_DEVICES=0,1,2,3;
vllm serve neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16 --trust-remote-code --max-model-len 8192 --tensor-parallel-size 4 --api-key token-abc123