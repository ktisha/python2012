# coding=utf-8
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

__NORMALIZER_SCRIPT = "./normalizer.sh"

def normalize_tag(tag):
    cmd = 'echo '+ tag + '|' + __NORMALIZER_SCRIPT
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    return p.stdout.read().replace("\n", "").split("+")

def normalize_bag_of_words(bag_of_words):
    FILE_FOR_NORMALIZER = "file_for_normalizer"
    FILE_FROM_NORMALIZER = "file_from_normalizer"

    with open(FILE_FOR_NORMALIZER, "w") as file:
        for word in bag_of_words:
            file.write(word.encode('utf-8') + "\n")

    subprocess.call('cat '+ FILE_FOR_NORMALIZER + '|' + __NORMALIZER_SCRIPT + '>' + FILE_FROM_NORMALIZER, shell = True)

    # with закроет файл даже если упадет исключение
    with open(FILE_FROM_NORMALIZER, "r") as file:
        result = map(str.strip, file.readlines())

    os.remove(FILE_FOR_NORMALIZER)
    os.remove(FILE_FROM_NORMALIZER)

    return result
