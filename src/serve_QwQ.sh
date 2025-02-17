#!/bin/bash

# Run with "bash serve_Llama405B.sh"
CUDA_VISIBLE_DEVICES=4,5,6,7;
vllm serve Qwen/QwQ-32B-preview --trust-remote-code --tensor-parallel-size 4 --api-key token-abc123 --port 8001