__author__ = 'sergio'

def input_text(filename):
    with open(filename, "r") as f:
        text = f.read()
    return text

def output_text(filename, text):
    with open(filename, "w") as f:
        print(text, f)
