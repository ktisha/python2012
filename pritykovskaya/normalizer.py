import subprocess

NORMALIZER_SCRIPT = "normalizer.sh"

def call_normalizer(file_for_normalizer, file_from_normalizer):
    subprocess.call('cat '+ file_for_normalizer + '|' + NORMALIZER_SCRIPT + '>' + file_from_normalizer, shell = True)
