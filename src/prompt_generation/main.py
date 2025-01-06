from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="token-abc123")

META_PROMPT = """
Given an existing prompt, produce a detailed user prompt to guide a language model in completing the task effectively.

The user prompt will ask the model to rewrite a provided PySpark code snippet to be compatible with Spark Connect.
It will provide the original code snippet, linter feedback, and context to help the model understand the task.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve Original Code: The input prompt will include the original code snippet. Preserve this code in the prompt. 
- Context: Don't  include context in the prompt directly. If the context is helpful to solve the task point out the relevant parts in the prompt.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly call out, that the output should only be the updated code snippet.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[The original code snippet]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Analysis of original code [optional]

[optional: a detailed explanation what the original code does and what exactly it outputs.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task. 
This should adress the issues in the original code pointed out by the linter and provide a clear path to a solution.]

# Output Format

[Specifically call out that the output should only be the updated code snippet]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
""".strip()


def generate_initial_prompt(code, linter_diagnostics, context):
    prompt = """We have a code snippet that is not compatible with Spark Connect. 
    Your task is to output code that is compatible with Spark Connect and maintains the same functionality and output.
    The code snippet is as follows:
    """
    prompt += code
    if linter_diagnostics:
        prompt += "\n\n## Linter Feedback\n"
        prompt += "The code was preprocessed by a linter. The detected problems are listed here:\n"
        for diag in linter_diagnostics:
            prompt += (
                f"- {diag['message']} at line {diag['line']}, column {diag['col']}\n"
            )
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
                "content": "Current Prompt:\n" + prompt,
            },
        ],
    )

    return completion.choices[0].message.content


def generate_iterated_prompt(adjusted_code, linter_diagnostics, context):
    prompt = """You were supposed to rewrite the provided PySpark code to be compatible with Spark Connect, 
    however, there are still some issues with the code. Please review the code snippet below and make the necessary adjustments to ensure it is compatible with Spark Connect. 
    The code snippet is as follows:"""

    prompt += "\n\n## Adjusted Version of Code (still contains issues)\n"
    prompt += adjusted_code
    if linter_diagnostics:
        prompt += "\n\n## Linter Feedback\n"
        prompt += "The code was preprocessed by a linter. The remaining problems are listed here:\n"
        for diag in linter_diagnostics:
            prompt += (
                f"- {diag['message']} at line {diag['line']}, column {diag['col']}\n"
            )
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
