############################################################
# CIS 521: Homework 8
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from string import punctuation, whitespace
import random
from math import *


############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    tokens = []
    current = ""
    for c in text:
        if c in whitespace or c in punctuation:
            if current:
                tokens.append(current)
                current = ""
            if c in punctuation:
                tokens.append(c)
        else:
            current += c
    
    if current:
        tokens.append(current)

    return tokens

def ngrams(n, tokens):
    extended = tokens + ["<END>"]
    ngrams = []

    def get_prev(index):
        if index < 0:
            return "<START>"
        return tokens[index]

    for index, token in enumerate(extended):
        prev = tuple([get_prev(index - i) for i in range(n - 1, 0, -1)])
        ngrams.append((prev, token))

    return ngrams

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.counts = dict()

    def update(self, sentence):
        for context, token in ngrams(self.n, tokenize(sentence)):
            if context not in self.counts:
                self.counts[context] = dict()
            self.counts[context][token] = self.counts[context].get(token, 0) + 1

    def prob(self, context, token):
        if context not in self.counts:
            return 0
        return self.counts[context].get(token, 0) / sum(self.counts[context].values())

    def random_token(self, context):
        if context not in self.counts:
            return None

        sorted_keys = sorted(self.counts[context].keys())
        sum_tokens = sum(self.counts[context].values())
        r = random.random()
        sum_p = 0
        for i in range(len(sorted_keys)):
            token = sorted_keys[i]
            sum_p += self.counts[context][token] / sum_tokens
            if sum_p > r:
                return sorted_keys[i]
        

    def random_text(self, token_count):
        start_context = tuple(["<START>"] * (self.n - 1))
        context = start_context
        tokens = []

        for _ in range(token_count):
            token = self.random_token(context)
            tokens.append(token)
            if token == "<END>":
                context = start_context
            elif self.n > 1:
                context = context[1:] + (token, )

        return " ".join(tokens)


    def perplexity(self, sentence):
        context = tuple(["<START>"] * (self.n - 1))
        
        log_sum = 0
        tokens = tokenize(sentence) + ["<END>"]
        for token in tokens:
            p = self.prob(context, token)
            log_sum += log(1 / p)
            if self.n > 1:
                context = context[1:] + (token, )

        return exp(log_sum) ** (1 / len(tokens))



def create_ngram_model(n, path):
    with open(path, "r") as f:
        m = NgramModel(n)
        for line in f.readlines():
            m.update(line)
        return m

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 1.5

feedback_question_2 = """
Nothing, no stumbling blocks
"""

feedback_question_3 = """
Everything was good!
"""
