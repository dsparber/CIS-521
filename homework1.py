############################################################
# CIS 521: Homework 1
############################################################

student_name = "Daniel Sparber"

############################################################
# Section 1: Python Concepts - Study Questions
############################################################

python_concepts_question_1 = """
Omitted
"""

python_concepts_question_2 = """
Omitted
"""

python_concepts_question_3 = """
Omitted
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [x for seq in seqs for x in seq]

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq) + 1):
        yield seq[:i]

def suffixes(seq):
    for i in range(len(seq) + 1):
        yield seq[i:]

def slices(seq):
    for start in range(len(seq) + 1):
        for end in range(start + 1, len(seq) + 1):
            yield seq[start:end]

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    return " ".join([word.lower() for word in text.split(" ") if word])

def no_vowels(text):
    return ''.join([c for c in text if c.lower() not in ['a', 'e', 'i', 'o', 'u']])

def digits_to_words(text):
    digits = {
        '1': "one",
        '2': "two",
        '3': "three",
        '4': "four",
        '5': "five",
        '6': "six",
        '7': "seven",
        '8': "eight",
        '9': "nine",
        '0': "zero"
    }
    return " ".join([digits[c] for c in text if c in digits.keys()])


def to_mixed_case(name):
    res = ''.join([part.lower().capitalize() for part in name.split('_') if part])
    if res:
        return res[0].lower() + res[1:0]
    return ""

############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.value = tuple(polynomial) 

    def get_polynomial(self):
        return self.value

    def __neg__(self):
        return Polynomial([(-k, x) for k, x in self.value])

    def __add__(self, other):
        return Polynomial(list(self.value + other.value))

    def __sub__(self, other):
        return Polynomial(list(self.value + (-other).value))

    def __mul__(self, other):
        result = []
        for k1, x1 in self.value:
            for k2, x2 in other.value:
                result.append((k1 * k2, x1 + x2))
        return Polynomial(result)

    def __call__(self, x):
        return sum([c * x**deg for c, deg in self.value])

    def simplify(self):
        values = dict()

        if self.value:
            for c, d in self.value:
                values[d] = c + values.get(d, 0)

        value = tuple(sorted([(c, d) for d, c in values.items() if c != 0], key=lambda t: -t[1]))
        
        if not value:
            value = tuple([(0, 0)])

        self.value = value

    def __str__(self):
        output = ""

        def to_str(c, d):
            if d == 0:
                return str(abs(c))
            if d == 1 and abs(c) == 1:
                return "x"
            if d == 1:
                return "{}x".format(abs(c))
            if abs(c) == 1:
                return "x^{}".format(d)
            return "{}x^{}".format(abs(c), d)
                
        
        for i in range(len(self.value)):
            c, d = self.value[i]

            if i == 0:
                if c >= 0:
                    output += to_str(c , d)
                else:
                    output += "-" + to_str(c, d)
            else:
                if c >= 0:
                    output += " + {}".format(to_str(c, d))
                else:
                    output += " - {}".format(to_str(c, d))
            
        return output

############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
2h
"""

feedback_question_2 = """
I did not find any parts challenging.
There were no stumbling blocks.
"""

feedback_question_3 = """
I liked the slicing exercise.
Nothing needs to be changed.
"""
