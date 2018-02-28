# -*-coding:utf-8 -*-

from ch2sql.tools.hit_ltp import LtpParser
from ch2sql.node import *


class Sentence(object):
    """
    对查询语言输入统一包装. 分词,词性标注, 实体识别的代码在LtpParser类中
    使查询语句的处理依赖但不耦合LTP工具
    """

    def __init__(self, sentence="一条测试语句", table=None):
        """
        :param sentence: 查询语句输入
        :param table: 查询对应的数据表格对象
        """
        self.parser = LtpParser
        self.table = table
        self._init_sentence = sentence
        self.sentence = Sentence.query_rewrite(sentence)
        self._tokens = list(self.parser.cutting(self.sentence, self.table))
        self._pos_tags = list(self.parser.pos_tagging(self.tokens))
        self._entities_list = list(self.parser.entity_recognize(self.tokens, self.pos_tags))
        self._dp_tree = self.parser.dependency_parsing(self.tokens, self.pos_tags)
        self.nodes = self.init_nodes()
        self.node_mapping()

    def drop(self, index):
        """
        drop token and nodes(since one token maps to one node)
        :param index: position of the node or token
        :return:
        """
        self._tokens.remove(self._tokens[index])
        self.nodes.remove(self.nodes[index])

    def init_nodes(self):
        ans = []
        for i in range(len(self.tokens)):
            ans.append(Node(self.tokens[i], self.table, self.pos_tags[i]))
        return ans

    @property
    def init_sentence(self):
        return self._init_sentence

    @property
    def tokens(self):
        return self._tokens

    @property
    def pos_tags(self):
        return self._pos_tags

    @property
    def entities_list(self):
        return self._entities_list

    @property
    def dp_tree(self):
        return self._dp_tree

    @staticmethod
    def query_rewrite(input_words):
        """
        对自然查询语句进行预处理进行预处理(查询改写模块)
        1. 将"比...大/高" 转换为 '大于...' 的形式
        2. 将"a 到 b 之间" 转化为 '大于等于a且小于等于b的形式'
        3. 将"比...小/低" 转换为 '大于...' 的形式
        ...
        :return: new_sentence
        """
        words = input_words

        # 匹配'比...好'的形式
        regex1 = re.compile(r'比(\w+)([大高多好])')
        words = re.sub(regex1, r'大于\1', words)

        # 匹配'比...低'的形式
        regex2 = re.compile(r'比(\w+)([低少差小])')
        words = re.sub(regex2, r'小于\1', words)

        # 匹配'a到b之间'的形式
        regex3 = re.compile(r'[在?](\w+|\d+)[到和与](\w+|\d+)之间')
        words = re.sub(regex3, r'小于\2并且大于\1', words)

        # 匹配'a到b间'的形式, 考虑如何上条和这一条进行合并
        regex3 = re.compile(r'[在?](\w+|\d+)[到和与](\w+|\d+)间')
        words = re.sub(regex3, r'小于\2并且大于\1', words)

        # TODO 错别字纠正

        # TODO ...
        return words

    def node_mapping(self):
        """
        token结果映射到数据库语义定义的节点中
        :return:
        """
        mapper = NodeMapper
        for node in self.nodes:
            possible_list = mapper.get_possible_node_info_list(node, self.table)
            new_list = [item for item in possible_list if item.score is not None and item.score > 0.5]
            # the node info with the highest score will be the nodeInfo of the node
            if len(new_list) == 1:
                node_info = new_list[0]
            elif len(new_list) > 1:
                sorted_list = sorted(new_list, reverse=True)
                if (sorted_list[0].score > 0.8) or sorted_list[0].score - sorted_list[1].score >= 0.2:
                    node_info = sorted_list[0]
                else:
                    node_info = NodeInfo(node.word, 'UN', ' ', 1)
            else:
                node_info = NodeInfo(node.word, 'UN', ' ', 1)
            node.nodeInfo = node_info

    def print_nodes(self):
        for node in self.nodes:
            print(node)


if __name__ == "__main__":
    s1 = "查询成绩比小明好的学生"
    s2 = "想知道比北京GDP低的城市"
    s3 = "GDP在北京和宁波之间的城市"
    print(Sentence.query_rewrite(s1))
    print(Sentence.query_rewrite(s2))
    print(Sentence.query_rewrite(s3))
