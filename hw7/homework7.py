############################################################
# CIS 521: Homework 7
############################################################

student_name = "Daniel Sparber"

############################################################
# Imports
############################################################

import homework7_data as data

# Include your imports here, if any are used.
from math import *



############################################################
# Section 1: Perceptrons
############################################################

class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.w = dict()

        for _ in range(iterations):
            for x, y in examples:
                yp = self.predict(x)
                if y != yp:
                    sign = 1 if y else -1
                    for i, xi in x.items():
                        self.w[i] = self.w.get(i, 0) + sign * xi


    def predict(self, x):
        value = sum([self.w.get(i, 0) * xi for i, xi in x.items()])
        return value > 0

class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        labels = set()
        for x, y in examples:
            labels.add(y)
        
        self.w = {l: dict() for l in labels}

        for _ in range(iterations):
            for x, y in examples:
                yp = self.predict(x)
                if y != yp:
                    for i, xi in x.items():
                        self.w[y][i] = self.w[y].get(i, 0) + xi
                        self.w[yp][i] = self.w[yp].get(i, 0) - xi
    
    def predict(self, x):
        value = None
        yMax = None
        for y, w in self.w.items():
            current = sum([w.get(i, 0) * xi for i, xi in x.items()])
            if value is None or current > value:
                value = current
                yMax = y
        return yMax


############################################################
# Section 2: Applications
############################################################

def tupleToDict(x):
    x = {i: v for i, v in enumerate(x)}
    x["bias"] = 1
    return x

def trianingToDict(data):
    return [(tupleToDict(x), y) for x, y in data]

class IrisClassifier(object):

    def __init__(self, data):
        self.classifier = MulticlassPerceptron(trianingToDict(data), iterations=50)

    def classify(self, instance):
        return self.classifier.predict(tupleToDict(instance))

class DigitClassifier(object):

    def __init__(self, data):
        self.classifier = MulticlassPerceptron(trianingToDict(data), iterations=15)

    def classify(self, instance):
        return self.classifier.predict(tupleToDict(instance))

class BiasClassifier(object):

    def __init__(self, data):
        with_bias = [({"bias": 1, "value": x}, y) for x, y in data]
        self.classifier = BinaryPerceptron(with_bias, iterations=10)

    def classify(self, instance):
        return self.classifier.predict({"bias": 1, "value": instance})


class MysteryClassifier1(object):

    @staticmethod
    def get_features(x):
        x1 = x[0]
        x2 = x[1]
        return {"bias": 1, "x1^2": x1**2, "x2^2": x2**2}

    def __init__(self, data):
        transformed = [(self.get_features(x), y) for x, y in data]
        self.classifier = BinaryPerceptron(transformed, iterations=10)

    def classify(self, instance):
        return self.classifier.predict(self.get_features(instance))


class MysteryClassifier2(object):

    @staticmethod
    def get_features(x):
        x1 = x[0]
        x2 = x[1]
        x3 = x[2]
        return {
            "x1x2x3": x1 * x2 * x3,
            }

    def __init__(self, data):
        transformed = [(self.get_features(x), y) for x, y in data]
        self.classifier = BinaryPerceptron(transformed, iterations=10)

    def classify(self, instance):
        return self.classifier.predict(self.get_features(instance))

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = 1.5

feedback_question_2 = """
Not challenging at all
"""

feedback_question_3 = """
Everything was fun
"""
