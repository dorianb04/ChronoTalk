import re

def prompt_splitter(prompt, max_length=250):
    # Split the prompt into sentences
    clean_prompt = prompt.replace('<br>', '').replace('\n', ' ').strip()
    clean_prompt = re.sub(r'(?<=\d)[.]', "", clean_prompt)
    sentences = re.split(r'(?<=[.!?]) +', clean_prompt)

    # Initialize variables
    current_length = 0
    current_prompt = ""
    prompts = []

    # Iterate over sentences and group them
    for sentence in sentences:
        if current_length + len(sentence) > max_length and current_prompt:
            prompts.append(current_prompt)
            current_prompt = ""
            current_length = 0

        current_prompt += sentence + " "
        current_length += len(sentence) + 1

    # Add the last prompt if it's not empty
    if current_prompt:
        prompts.append(current_prompt.strip())

    return prompts