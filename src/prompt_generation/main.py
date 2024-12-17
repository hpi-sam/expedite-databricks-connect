from openai import OpenAI
from omegaconf import DictConfig
from typing import List, Dict


client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")

META_PROMPT = """
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
""".strip()


def generate_initial_task_description(code, linter_diagnostics, context):
    prompt = """We have a code snippet that is not compatible with Spark Connect. 
    Please describe in detail what this code does and what the expected output is.
    Now identify the issues in the code that make it incompatible with Spark Connect and describe how you would fix them.
    Dont implement the changes, just describe them.
    The code snippet is as follows:
    """
    prompt += code
    if linter_diagnostics:
        prompt += "\n\n## Linter Feedback\n"
        prompt += "The code was preprocessed by a linter. The detected problems are listed here:\n"
        for diag in linter_diagnostics:
            prompt += f"- {diag['message']} at line {diag['line']}, column {diag['col']}\n"
    if context:
        prompt += f"\n\n## Context\n"
        prompt += "In case it is helpful you can use the following context to help you with the task: \n"
        prompt += str(context)

    completion = client.chat.completions.create(
    model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
    messages=[
            {
                "role": "system",
                "content": META_PROMPT,
            },
            {
                "role": "user",
                "content": "Task, Goal, or Current Prompt:\n" + prompt,
            },
        ],
    )

    return completion.choices[0].message.content


def generate_initial_prompt(code, linter_diagnostics, context):
    prompt = """Rewrite the provided PySpark code to be compatible with Spark Connect, 
    ensuring the rewritten code maintains the same functionality and output as the original code. The code snippet is as follows:"
    """
    prompt += code
    prompt += "Here is a more detailed description of the task:\n"
    prompt += generate_initial_task_description(code, linter_diagnostics, context)
    prompt += """Return the rewritten code snippet.
        * Do not change the function signature or name.
        * Do not add any code outside the existing function.
        * Ensure the rewritten code has the same functionality and output as the original code.
        """
    return prompt


def generate_iterated_prompt(original_code, adjusted_code, linter_diagnostics, context):
    prompt = """You were supposed to rewrite the provided PySpark code to be compatible with Spark Connect, 
    however, there are still some issues with the code. Please review the code snippet below and make the necessary adjustments to ensure it is compatible with Spark Connect. 
    The code snippet is as follows:"""
       
    prompt += "\n\n## Adjusted Version of Code (still contains issues)\n"
    prompt += adjusted_code
    if linter_diagnostics:
        prompt += "\n\n## Linter Feedback\n"
        prompt += "The code was preprocessed by a linter. The remaining problems are listed here:\n"
        for diag in linter_diagnostics:
            prompt += f"- {diag['message']} at line {diag['line']}, column {diag['col']}\n"
    if context:
        prompt += f"\n\n## Context\n"
        prompt += "In case it is helpful you can use the following context to help you with the task: \n"
        prompt += str(context)

    completion = client.chat.completions.create(
    model="neuralmagic/Meta-Llama-3.1-405B-Instruct-quantized.w4a16",
    messages=[
            {
                "role": "system",
                "content": META_PROMPT,
            },
            {
                "role": "user",
                "content": "Task, Goal, or Current Prompt:\n" + prompt,
            },
        ],
    )

    return completion.choices[0].message.content
    
    


