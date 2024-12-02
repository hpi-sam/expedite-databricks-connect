# 🚀 Llama-powered RAG Approach for Spark to Spark Connect Migration

This project provides a **Retrieval-Augmented Generation (RAG)** pipeline to assist in migrating PySpark code from classic Spark to **Spark Connect**. It uses **LangChain** and **Llama** to process documentation and generate updated code.

---

## 🛠️ Setup

### 1️⃣ Environment Setup
We use `conda` for environment management. The dependencies are listed in `environment.yml`.

#### Create the Environment
```bash
conda env create -f environment.yml
```

Optionally add ```-n <name>```

#### Activate the Environment
```bash
conda activate <name>
```

#### Update the Environment
```bash
conda env update --file environment.yml --prune
```

#### Deactivate the Environment
```bash
conda deactivate
```

#### Delete the Environment
```bash
conda remove --name <name> --all
```

### 2️⃣ Setting Up GitHub Access
To load code from GitHub repositories, you need a GitHub Personal Access Token.

1. Go to [GitHub Tokens Page](https://github.com/settings/tokens).
2. Click Generate new token, set the custom expiry date as far in the future as possible (up to 1 year), and copy the token. 

3. Add it to your ~/.bashrc file, following these steps:
```bash
echo 'export GITHUB_ACCESS_TOKEN=<YOUR_TOKEN>' >> ~/.bashrc
source ~/.bashrc
```

## 📂 Project Structure
- docs - documentation about the setup and the different components of the project
- resources - relevant papers and other resources used for research
- environment.yml - Lists all dependencies for the project.
- src - the code of the project
- src/evaluation - the code used to evaluate the performance of the automated code generation
- src/linter - code for a linter, the can be used to identify code that is not compatible with spark connect
- src/vector_store - code to create a vectorstor e.g from spark documentation or github repositorys that is used to provide context to the llm model according to the rag approach
- src/main.py - the main script that will run the evaluation pipeline with a code generation configured in config.py

## 🎯 Usage

To run the code migration you first need to make the cuda devices visible. 
```bash
CUDA_VISIBLE_DEVICES=0,1,2,3;
```
Then run a served version of the LLM with this script `serve_Llama405B.sh`.

You also need a Spark Connect Server running. You can download Spark with this command 
```bash
wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-hadoop3.tgz
```

and unpack the folder with 
```bash
tar xvf spark-3.5.3-bin-hadoop3.tgz 
```
In the `sbin` folder you will find the script to start a Spark Connect server. Run it with 
```bash
bash start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.3
```
Now you can start the evaluation pipeline by going to the src folder and running `python main.py`.
To migrate a single pice of code you can call the function ```migrate_code``` from src/main.py.

## 📋 Notes
- The script uses neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16 as the LLM.
- It is recommended to use quantized models for efficient inference.
- GPU usage is necessary for Llama-3.1, and very powerful GPUs like the H100 are recommended. You need multiple GPUs.


