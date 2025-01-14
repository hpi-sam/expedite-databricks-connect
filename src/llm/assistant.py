import os
from typing import List, Dict
from omegaconf import DictConfig
from transformers import PreTrainedTokenizerFast, AutoTokenizer
from openai import OpenAI
from huggingface_hub import login


class Assistant:
    model_name: str
    temperature: float
    _client: OpenAI
    _system_message: Dict[str, str]
    _messages: List[Dict[str, str]]
    _tokenizer: PreTrainedTokenizerFast

    def __init__(self, model_temperature: float, cfg: DictConfig):
        login(token="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")
        self._client = OpenAI(base_url=os.getenv("VLLM_BASE_URL"))
        self._system_message = {
            "role": "system",
            "content": cfg.system_prompt,
        }
        self._messages = []
        self.temperature = model_temperature
        self.model_name = cfg.model_name
        self._tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
        assert (
            self._tokenizer != False
        ), f"somthing went wrong when fetching the default tokenizer for model {cfg.model_name}"

    def _all_messages(self):
        return [self._system_message] + self._messages

    def _tokenized_messages(self):
        return self._tokenizer.apply_chat_template(self._all_messages(), tokenize=True)

    def generate_answer(self, prompt: str, cfg: DictConfig) -> str:
        self._messages += [
            {"role": "user", "content": prompt},
        ]
        num_tokens = len(self._tokenized_messages())
        while num_tokens > cfg.max_model_length - cfg.answer_token_length:
            self._messages.pop(0)
            num_tokens = len(self._tokenized_messages())

        completion = self._client.completions.create(
            model=self.model_name,
            max_tokens=cfg.answer_token_length,
            prompt=self._tokenized_messages(),
            temperature=self.temperature,
        )
        answer = completion.choices.pop().text
        self._messages += [
            {
                "role": "assistant",
                "content": answer,
            }
        ]
        return answer
