import os
from ch2sql.tools import synonyms
import importlib

"""
  载入哈工大同义词表
"""
import ch2sql

# 哈工大近义词表
hit_source_file = os.path.join(ch2sql.__file__[:-12], "lib/hit_simi_words.txt")
# 载入停用词表,这里暂时使用四川大学停用词表
stopwords_file = os.path.join(ch2sql.__file__[:-12], "lib/stopwords.txt")
loaded = False
_synonyms_dict = {}
_id_dict = {}
stopwords = []
flag = True
load_stopwords_flag = False


def load():
    """
    载入哈工大同义词表
    :return:
    """
    with open(hit_source_file, encoding='utf-8') as f:
        for line in f:
            line = line[:-1]
            tmp = line.split(' ')
            assert len(tmp) > 1, 'len(line) must > 0'
            id = tmp[0]
            # last character of 'id' is '='
            if id[-1] == '=':
                if id not in _synonyms_dict:
                    _synonyms_dict[id] = []
                for i in range(1, len(tmp)):
                    _synonyms_dict[id].append((tmp[i], id))
                    _id_dict[tmp[i]] = id
            elif id[-1] == '#':
                pass
            elif id[-1] == '@':
                pass
            else:
                pass
        global loaded
        loaded = True
        print("hit-synonyms lib file loaded")


def load_stopwords():
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line[:-1]
            stopwords.append(line)
    global load_stopwords_flag
    load_stopwords_flag = True


def is_stopwords(word):
    global load_stopwords_flag
    if not load_stopwords_flag or stopwords is None:
        load_stopwords()
    if word in stopwords:
        return True
    else:
        return False


def std_word(word):
    """
    :param word:
    :return: the standard synonym of this word(only one word)
    """
    global loaded
    if not loaded:
        load()
    if word in _id_dict:
        return _synonyms_dict[_id_dict[word]][0][0]
    else:
        return word


def synonyms_list(word):
    """
    :param word:
    :return: 同义词表中word的同义词
    """
    global loaded
    if not loaded:
        load()
    if word not in _id_dict:
        print("no synonyms for {}".format(word))
    else:
        return [tup[0] for tup in _synonyms_dict[_id_dict[word]]]


def _levenshtein_distance(sentence1, sentence2):
    '''
    Return the Levenshtein distance between two strings.
    Based on:
        http://rosettacode.org/wiki/Levenshtein_distance#Python
    '''
    first = sentence1
    second = sentence2
    if len(first) > len(second):
        first, second = second, first
    distances = range(len(first) + 1)
    for index2, char2 in enumerate(second):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(first):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1],
                                              distances[index1 + 1],
                                              new_distances[-1])))
        distances = new_distances
    levenshtein = distances[-1]
    return 2 ** (-1 * levenshtein)


def similar_scores(word1, word2):
    """
    使用词向量表示计算两个词之间的语义相似度
    :return: word1 和 word2的语义相似度得分(最大 1.0)
    """
    global flag
    if flag:
        import jieba
        importlib.reload(jieba)
        flag = False
    return synonyms.compare(word1, word2)


def edit_distance_score(word1, word2):
    return _levenshtein_distance(word1, word2)


if __name__ == "__main__":
    pass
