import os.path as path
from transformers import pipeline


def profanity_replace(input):
    """
    This function takes a string as input and checks if any word in the string
     is a profanity word. If a profanity word is found, it replaces the word
    with '*' of the same length.
    At the moment, we are using words from this list:
    https://github.com/coffee-and-fun/google-profanity-words/tree/main

    :param input: string
    :return: dictionary with keys: message, profanity_found, successful
    """
    try:
        # Input validation
        if isinstance(input, int):
            input = str(input)
        if not isinstance(input, str):
            raise TypeError

        # Read the profanity list
        dir_path = path.dirname(path.realpath(__file__))
        with open(
            path.join(dir_path, 'config/profanity_list.txt'),
            'r',
        ) as file:
            profanity_list = file.read()
            profanity_list = [
                line.strip() for line in
                profanity_list.splitlines() if line.strip()
            ]
            file.close()

        # Check if any profanity word is present in the input
        flag = False
        for word in profanity_list:
            if word in input:
                flag = True
                input = input.replace(word, '*' * len(word))

        return {
            'message': input,
            'profanity_found': flag,
            'successful': True,
        }
    except FileNotFoundError:
        return {
            'message': 'Profanity list not found',
            'profanity_found': False,
            'successful': False,
        }
    except TypeError:
        return {
            'message': 'The input is not Valid',
            'profanity_found': False,
            'successful': False,
        }


def load_text_classification_pipeline():
    """
    This function loads the text classification toxic bert pipeline
    from the Hugging Face. More details can be found here:
    https://huggingface.co/unitary/toxic-bert

    return: pipeline object
    """
    try:
        # Load the pipeline
        pipe = pipeline("text-classification", model="unitary/toxic-bert")

        # Load it to the memory, to make sure it's fast
        pipe("This is a test")
        return pipe
    except Exception:
        return None
