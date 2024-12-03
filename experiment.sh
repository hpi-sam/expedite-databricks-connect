#!/bin/bash

python rag_experiment.py --use_rag True --rag_store /raid/smilla.fox/vector_store_large
python rag_experiment.py --use_rag True --rag_store /raid/smilla.fox/vector_store
python rag_experiment.py --use_rag True --rag_store /raid/smilla.fox/vector_store_splits
python rag_experiment.py --use_rag True --rag_store /raid/smilla.fox/vector_store_splits --rag_num_docs 2
python rag_experiment.py --use_rag False
