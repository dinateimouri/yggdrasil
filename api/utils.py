import os.path as path
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


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


def detect_harmful_content(pipe, input_text):
    """
    This function takes a string as input and checks if the input text is
    harmful.
    If the input text is harmful, it returns the probability of harmfulness.
    If the input text is not harmful, it returns 0.

    :param pipe: pipeline object
    :param input_text: string
    :return: float
    """
    try:
        # Input validation
        if isinstance(input_text, int):
            input_text = str(input_text)
        if not isinstance(input_text, str):
            raise TypeError
        if isinstance(pipe, pipeline):
            raise TypeError

        # Check if the input text is harmful
        output = pipe(input_text)
        if output[0]['label'] == 'toxic':
            return output[0]['score']
        else:
            return None
    except TypeError:
        return None
    except Exception:
        return None


def similarity_cosine(input_list):
    """
    This function takes a list of strings as input and calculates the cosine
    similarity between the strings.
    The function returns a dictionary with keys: successful, similarity_matrix.

    :param input_list: list of strings
    :return: dictionary with keys: successful, similarity_matrix
    """

    try:
        # Input validation
        if not isinstance(input_list, list):
            raise TypeError
        if len(input_list) < 2:
            raise TypeError
        if not all(isinstance(x, str) for x in input_list):
            raise TypeError
        if len(set(input_list)) == 1:
            return {
                "successful": True,
                "similarity_matrix":
                {
                    input_list[0]: {
                        input_list[0]: 1.0,
                    },
                },
            }

        # Convert the texts to TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(input_list)

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Display the results as a DataFrame for better readability
        cosine_sim_df = pd.DataFrame(
            cosine_sim,
            index=input_list,
            columns=input_list,
        )

        # Output the cosine similarity matrix
        output = {}
        output['successful'] = True
        output['similarity_matrix'] = cosine_sim_df.to_dict()

        return output

    except TypeError:
        return {"successful": False, "similarity_matrix": None}
