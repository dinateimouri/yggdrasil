# Lessons Learned

This document aims to discuss challenges I faced during design and implementation of this assignment.

## API Design

At the moment, all of these packages and functions are implemented inside the API container, this leads to have a fat container with 8 GB of data. The main reason behind this is due to time limit I have. The best practice is to separate them into one or more container and leave API as a tiny service capable of handling thousands of requests.

## Ollama and Llama3.2:1b

The main reason for using Ollama and Llama3.2:1b is to be able to run them on my local machine.  This leads to have poor performance tests results. If there is a need to change it, it can be done simply as it follows the same principles.

## Code quality over time

As the deadline is/was approaching rather quickly and I have limited time, the code quality might worsen over time. So please take a look at my earlier commits to get to know my work quality better.

## Future works and how it can be improved

The very first improvement that comes to my mind and seems required, is to separate the sanitization algorithms from API itself. And the second one, would be to improve the code quality. And finally there is a list of nice to haves in [the epic list](https://github.com/dinateimouri/yggdrasil/issues/1), and I feel the `/async-chat` is one of the important ones (read about it [here](https://github.com/dinateimouri/yggdrasil/issues/15)).

## Filtering out disallowed words/phrases

First of all, this function is implemented in [api/utils.py](./api/utils.py) as `profanity_replace()`.
Before diving into implementation, I investigated to learn more about what it is and how it should be
implemented. There are several blog posts about having such feature and some experiences and I found
[this comment in stackoverflow](https://stackoverflow.com/a/273520) very inspiring.

Generally speaking, there are various methods for such filtering described in
[this comment](https://stackoverflow.com/a/13447680), and can be summarized as:

- Basic filtering
    - Implement a search function to search the input string in a predefined list of profanities.
        - Two nested for loops
        - [Aho Corasik Algorithm](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm)
    - Implement a method of dealing with derivations of profanities.
- Moderately complex filtering
    - Using complex pattern matching to deal with extended derivations (using advanced regex)
    - Implement a method to deal with Leetspeak
    - Implement a method to deal with false positives
- A complex filter
    - Implement Allow list and block list
    - Implement a [Naive bayesian inference](https://en.wikipedia.org/wiki/Bayesian_inference) filtering of phrases/terms
    - Implement [Soundex functions](https://en.wikipedia.org/wiki/Soundex) (where a word sounds like another)
    - Implement [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
    - Implement [Stemming](https://en.wikipedia.org/wiki/Stemming)
    - Human moderators to help guide a filtering engine to learn by example
- The most complicated filters
    - Use other AI/ML techniques

### Design Decision

I chose to implement a basic filtering using a nested for loop search function for the very first version due to limited implementation time. Moreover, more complex tasks can take longer thus they may need to be located in a microservice other
than API for scalability purposes.

## Handle harmful content

When talking about handling harmful content, we need to analyze the context, tone and meaning of the text.
There are various method for such analysis such as:

- [Sentiment Analysis](https://en.wikipedia.org/wiki/Sentiment_analysis): This method is widely used to
interpret the emotional tone of the text (positive, negative, neutral). [TextBlob](https://textblob.readthedocs.io/en/dev/) seems to be a relevant
library for it.
- Train a classifier model on a labeled dataset to classify text to harmful or non-harmful. This might be
the best available approach if the usecase is in a pre-defined context. But it needs to have such dataset
and resources such as hardware and time.
- Using a pre-trained and fine-tuned models such as [toxic-bert](https://huggingface.co/unitary/toxic-bert)
from [Unitary](https://www.unitary.ai/). This model is able to understand the context of words. And it's already trained on [Wikipedia Toxic Comments dataset](https://figshare.com/articles/dataset/Wikipedia_Talk_Labels_Toxicity/4563973).

### Design Decision

I chose to implement the third option and use the pre-trained model listed above due to limited time for this
assignment. Moreover, the [transformers](https://github.com/huggingface/transformers) library seems more stable than other libraries.

## Similarity measures

There are various similarity measures out there. For most of them, they need to be vectorized the input text and then execute the desired similarity measure. These similarity measures can be listed as follows (but it's not limited to this list):

- Cosine distance
- Manhattan distance
- Euclidean distance
- Haversine distance
- Jaccard distance
- Minkowski distance
- Chebyshev distance
- And many more

### Design decision

I chose to work with the first three similarity measures as they seem to be more popular and there are various well-maintained libraries implementing them efficiently. For this I used `scikit-learn` library.
