import sys
import pytest
sys.path.append('..')
from ch2sql import database


def test1():
    col = database.Column()
    col.print_me()

def test_syn():
    word1 = "中国"
    word2 = "日本"
    import synonyms
    print(synonyms.compare(word1, word2))

