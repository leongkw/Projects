1. Introduction
This NLP module is currently still in developmental phase. When operational, it will serve as the NLP engine for a chatbot that will provide learning assistance to its user.

Currently, there are a few issues that present that is slowing developmental progress:
(i) Lack of data - Everything is self fabricated here; one of the barriers to using more powerful models, unable to carry out train-test split & testing
(ii) Length of each document - One of the barriers to using more sophisticated word embedding techniques
(iii) Personal inexperience

The end goal (in the actual project) is for this to be built into a backend NLP service bot.
User text input --> Frontend Bot --> NLP Service Bot --> Frontend Bot --> Output text to user 

Note: Model.bin is omitted due to its large file size (800~MB)
2. Flow
- Input text comes in from user
- Input text is classified into its appropriate category via fasttext model
- Input text is added into the corpus of its classified category
- Corpus is vectorized using Tfidf Vectorizer
- Cosine similarity between input text and other documents in corpus is calculated, returning the output of document with the highest cosine similarity