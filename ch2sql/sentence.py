# -*-coding:utf-8 -*-

from ch2sql.database import Table
from ch2sql.tools.hit_ltp import LtpParser
from ch2sql.node import *
import heapq

class Sentence(object):
    """
    对查询语言输入统一包装. 分词,词性标注, 实体识别的代码在LtpParser类中
    使查询语句的处理依赖但不耦合LTP工具
    """

    def __init__(self, sentence="这是一条测试语句", table=None):
        """
        :param sentence: 查询语句输入
        :param table: 查询对应的数据表格对象
        """
        self.parser = LtpParser
        self.table = table
        self._init_sentence= sentence
        self.sentence = Sentence.query_rewrite(sentence)
        self._tokens = list(self.parser.cutting(self.sentence, table))
        self._pos_tags = list(self.parser.pos_tagging(self.tokens))
        self._entities_list = list(self.parser.entity_recognize(self.tokens, self.pos_tags))
        self._dp_tree = self.parser.dependency_parsing(self.tokens, self.pos_tags)
        self.nodes = self.init_nodes()

    def init_nodes(self):
        ans = []
        for i in range(len(self.tokens)):
            ans.append(Node(self.tokens[i], self.table, self.pos_tags[i]))
        return ans

    @property
    def words(self):
        return self._words

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
        regex1 = re.compile(r'(\w*)比(\w+)([大高多好])')
        if regex1.match(words):
            words = regex1.sub(r'\1大于\2', words)
            return words

        # 匹配'比...低'的形式
        regex2 = re.compile(r'(\w*)比(\w+)([低少差小])')
        if regex2.match(words):
            words = regex2.sub(r'\1小于\2', words)
            return words

        # 匹配'a到b之间'的形式
        regex3 = re.compile(r'(\w*)[在?](\w+|\d+)[到和与](\w+|\d+)之间')
        if regex3.match(words):
            words = regex3.sub(r'\1小于\3并且大于\2',words)
            return words

        # 匹配'a到b间'的形式, 考虑如何上条和这一条进行合并
        regex3 = re.compile(r'(\w*)[在?](\w+|\d+)[到和与](\w+|\d+)间')
        if regex3.match(words):
            words = regex3.sub(r'\1小于\3并且大于\2', words)
            return words

        # TODO 错别字纠正

        # TODO ...

    def node_mapping(self):
        mapper = NodeMapper
        for node in self.nodes:
            possible_list = mapper.get_possible_node_info_list(node, self.table)
            new_list = [item for item in possible_list if item.score is not None and item.score > 0.5]
            # the node info with the highest score will be the nodeInfo of the node
            if len(new_list) == 1:
                nodeInfo = new_list[0]
            elif len(new_list) > 1:
                sorted_list = sorted(new_list,reverse=True)[0]
                if sorted_list[0].score - sorted_list[1].score >= 0.2:
                    nodeInfo = sorted_list[0]
                else:
                    nodeInfo = NodeInfo(node.word, 'UN',' ',1)
            else:
                nodeInfo = NodeInfo(node.word, 'UN',' ',1)
            node.nodeInfo = nodeInfo

    def print_nodes(self):
        for node in self.nodes:
           print(node)

if __name__ == "__main__":
    s1 = "比小明成绩差"
    s2 = "比北京GDP低"
    s3 = "在30和40之间"
    print(Sentence.query_rewrite(s1))