# Lessons Learned

This document aims to discuss challenges I faced during design and implementation of this assignment.

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
