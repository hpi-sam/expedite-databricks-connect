from vllm import LLM, SamplingParams
from transformers import AutoTokenizer

model_id = "neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16"
number_gpus = 4
max_model_len = 4096

sampling_params = SamplingParams(temperature=0.9, top_p=0.9, max_tokens=256)

tokenizer = AutoTokenizer.from_pretrained(model_id)

messages = [
    {
        "role": "system",
        "content": "You are a chatbot who deeply knows every person in the world and can answer any question about them.",
    },
    {
        "role": "user",
        "content": "Who is Smilla Fox? She lives in Berlin and is studying IT-Systems Engineering at the HPI (University of Potsdam).",
    },
]

prompts = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True, tokenize=False
)

llm = LLM(model=model_id, tensor_parallel_size=number_gpus, max_model_len=max_model_len)

outputs = llm.generate(prompts, sampling_params)

generated_text = outputs[0].outputs[0].text
print(generated_text)
