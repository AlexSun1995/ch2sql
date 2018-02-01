# -*-coding:utf-8 -*-
import jieba
from ch2sql.database import Table
import sys
from ch2sql.tools.hit_ltp import LtpParser
from ch2sql.node import *


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
        self._sentence = sentence
        self._tokens = list(self.parser.cutting(sentence, table))
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

    def node_mapping(self):
        mapper = NodeMapper
        for node in self.nodes:
            possible_list = mapper.get_possible_node_info_list(node, self.table)
            new_list = [item for item in possible_list if item.score is not None and item.score > 0.5]


