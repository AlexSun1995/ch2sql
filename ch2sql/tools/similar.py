import os
import synonyms
"""
  载入哈工大同义词表
"""
import ch2sql
hit_source_file = os.path.join(ch2sql.__file__[:-12], "lib/hit_simi_words.txt");
loaded = False
_synonyms_dict = {}
_id_dict = {}

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


def similar_scores(word1, word2):
    """
    使用词向量表示计算两个词之间的语义相似度
    :return: word1 和 word2的语义相似度得分(最大 1.0)
    """
    return synonyms.compare(word1, word2)


if __name__ == "__main__":
    print(std_word("浙江"))
    print(std_word("大学"))
    print(std_word("尚未"))
    print(synonyms_list("北京市"))
    import jieba
    s = "北京市今天的最高气温"
    li = list(jieba.cut(s))
    new_li = [std_word(word) for word in li]
    print(new_li)
    word1 = "杭州"
    word2 = "杭州市"
    print(similar_scores(word1, word2))