###text_spliter.py###

def prompt_splitter(input_str, max_length=250):
    if len(input_str) <= max_length:
        return [input_str]

    substrings = []
    current_substring = ""
    words = input_str.split()

    for word in words:
        if len(current_substring) + len(word) + 1 <= max_length:
            current_substring += " " + word
        else:
            substrings.append(current_substring.lstrip())
            current_substring = word

    if current_substring:
        substrings.append(current_substring)

    return substrings


