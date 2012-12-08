-DESCRIPTION-
pylm is a simple program for creating Language models from text corpora.
It uses Good-Turing smoothing.

-USAGE-
python LM.py [-c <path>] [-lm <out_file>] [-o <max_order>] [-gt <good-turing parameters>]

Parameters:
    -c   - set path to text corpora - a folder with .txt files of english texts. pylm runs through the folder recursively
        default: '.'
    -lm  - set the output language model file
        default: 'lm.txt'
    -o   - set maximum language model order
        default: 3
    -gt  - set good-turing smoothing parameters (gtNmin). It's a comma-separated list of numbers.
        Each number corresponds to certain order of ngrams. Smoothing is used for those
        ngrams only, which have absolute count less than the provided gtNmin parameter.
        default: 1 (one) for all orders

-EXAMPLE-
python LM.py -c 'data' -lm 'model.txt' -o '5' -gtNmin 3,2,2,1,1

This command runs building language model from .txt files inside 'data' directory (and it's subdirectories).
The output file will be 'model.txt'. Order of the model is 5.
Smoothing is used for unigrams with absolute counts less than 3,
bigrams with absolute counts less than 2,
trigrams with absolute counts less than 1,
etc.

-OUTPUT-
The output langage model is written in ARPA language model format.
The file begins with '\data\' line, which is followed by several lines, containing counts of distinct
ngrams for each order.
Next follows the line '\1-grams:', followed by a block of sorted unigrams.
Than goes '\2-grams:' line, followed by a block of sorted bigrams.
And so on.
The last line of the file contains '\end\' string.
Each n-gram line contains log10 probability, the n-gram and a back-of-weight (though the last one
is always zero, as it isn't computed in pylm).
The n-grams of maximum order can't have back of weights, so they're missing.
