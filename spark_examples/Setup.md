# Setup Evaluation Example

## Requirements
- `conda install python-dotenv`
- `conda install pyspark`
- `conda install groq`

To use the example with Groq add your Groq API-Key to a .env file.
You only need these requirements for the Groq example.

## Usage
Start a Spark-Connect server with `bash start-connect-server.sh --packages org.apache.spark:spark-connect_2.12:3.5.3`.
(Only necessary while linter isn't integrated yet)



Run `python groq_example.py` to run the evaluation example with groq.

You can also use the evaluation with other models and scripts. For this you can use the `evaluation` function from `evaluate.py`and give it your generation function as input. The generation function should have two parameters. The first is the code that will be transformed by the model in string format and the second is the function that is being evaluated. This function can be used to produce the corresponding error message for the LLM promt (will be replaced by the linter). The generation function should output the LLMs output.




