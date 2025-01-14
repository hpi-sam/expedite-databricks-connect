#!/bin/bash

# Run with "bash serve_Llama405B.sh"
CUDA_VISIBLE_DEVICES=4,5,6,7;
vllm serve Qwen/Qwen2.5-Coder-32B-Instruct-AWQ --trust-remote-code --tensor-parallel-size 4 --api-key token-abc123 --port 8001