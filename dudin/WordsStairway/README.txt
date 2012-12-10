WordsStairway README
==================


Description
-----------

This program created a 'stairway' between 2 words: a chain of transformation,
in which next transformation changes from previous only in 1 symbol, and each
transformation step should be an element from defined dictionary.

Program creates stairway with minimal number of transformations.
Its algorithm uses analog of breadth-first search (bfs) in graphs.
For more information about bfs, look here:
http://en.wikipedia.org/wiki/Breadth-first_search


Getting Started
---------------

- cd <directory containing this file>

- Into 'any_file_with_target_words.txt' write start_word and end_word
  (firstly start_word, then end_word, with Space or NewLine between them, nothing else)
  For example, look through existing 'target_words.txt'

- python Main.py any_file_with_target_words.txt