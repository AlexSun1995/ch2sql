# -*-coding:utf-8 -*-
import jieba
from ch2sql.database import Table
import sys


class Sentence(object):
    """
    对查询语言处理、提取需要的信息统一包装
    """
    default_ltp_api_key = "s1n5k7M9i5zXTqamAy3V1U7CkwskygraFX5fpKyH"

    def __init__(self, sentence="这是一条测试语句", db_info=None):
        # db_info 包括下面几种类型
        # 1. db_info 为包含字段名和数据类型信息的json格式数据
        # 2. 在1所包含的信息以外，还有数据表中的数据信息
        self.sentence = sentence
        self.db_info = db_info

    @staticmethod
    def cutting(sentence, table=None):
        """
        :param sentence: 输入的查询语句
        :param table: 数据表格对应的Table
        :return: 分词结果
        """
        # 根据数据库字段信息更新jieba分词词典,确保表的关键词不能分开
        if table is None:
            return list(jieba.cut(sentence))
        suggest_words = list(table.get_column_names())
        ans = None
        for column in table:
            if column.data_type != "text":
                continue
            tmp = column.values_sample(100)
            for v in tmp:
                suggest_words.append(v)
        print(suggest_words)
        for word in suggest_words:
            if word != " " and word is not None:
                jieba.suggest_freq(word, True)
        ans = list(jieba.cut(sentence, HMM=True))
        return ans

    @staticmethod
    def pos_tagging(cutting_list):
        pass

    @staticmethod
    def entity_recognize(cutting_list, tagging_list):
        pass

    @staticmethod
    def dependency_parsing(cutting_list, tagging_list):
        pass

    def info_wrapper(self):
        pass

    @staticmethod
    def getting_by_cloud(sentence, api_key=default_ltp_api_key, pattern='dp'):
        """
        调用语言云进行分词、词性标注、命名实体识别。
        http://api.ltp-cloud.com/
       （测试阶段使用，调用语言云就不能更新分词词典）
        :param sentence:
        :param api_key:
        :param pattern: ws: 分词, pos:词性标注, ner: 命名实体识别
        dp:依存语法分析, srl:语义角色标注
        :return:
        """
        import urllib.parse
        import urllib.request
        url_get_base = u"http://api.ltp-cloud.com/analysis/?"
        args = {
            'api_key': api_key,
            'text': sentence,
            'pattern': pattern,
            'format': 'plain'
        }
        url = url_get_base + urllib.parse.urlencode(args)
        # print(url)
        result = urllib.request.urlopen(url)
        content = result.read().strip()
        return content.decode('utf-8')

    @staticmethod
    def getting_all_by_cloud(sentence):
        patterns = ['ws', 'pos', 'ner', 'dp', 'srl']
        for pattern in patterns:
            result = Sentence.getting_by_cloud(sentence, pattern=pattern)
            print('pattern type:{}'.format(pattern))
            print(result)


if __name__ == '__main__':
    Sentence.getting_all_by_cloud("三月份的平均气温大于北京的城市")
