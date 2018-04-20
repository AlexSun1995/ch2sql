from ch2sql.node import *


class ExpandAN(object):
    """

     将 Attribute Node 单独提取出来
     目的是将 聚集函数, Group by 等描述属性节点的节点合并到AN中
     使之成为一个整体

    """

    def __init__(self, an, d_type):
        if type(an) != Node:
            raise Exception("构造参数类型不是Node")
        self.an = an
        self.attribute_name = an.nodeInfo.symbol
        # 属性节点需要有对应的数据类型
        self.attribute_type = d_type
        self.group_by = False
        self.function_nodes = []
        self.value_nodes = []
        self.top_node = None
        self.is_single = True
        self.nodes_index = []

    def add_group_by_node(self):
        self.group_by = True
        self.is_single = False

    def add_function_node(self, f):
        self.function_nodes.append(f)
        self.is_single = False

    def add_top_node(self, top_value):
        self.top_node = top_value
        self.is_single = False

    def add_nodes_index(self, index):
        self.nodes_index.append(index)
        self.is_single = False

    def add_value_nodes(self, vn):
        self.value_nodes.append(vn)
        self.is_single = False

    def sort_function_nodes(self):
        """
        function node 不止一个的时候需要对这些nodes进行排序
        :return:
        """
        pass

    def is_single_node(self):
        """
        如果当前节点没有和其他节点聚合 只是一个单纯的attribute node
        :return: True
        """
        return self.is_single

    def __str__(self):
        self.sort_function_nodes()
        ans = ''
        print(self.function_nodes)

        if self.is_single_node():
            ans = self.attribute_name
        else:
            if len(self.function_nodes) > 0:
                for f in self.function_nodes:
                    ans = ans + str(f) + '('
                ans += self.attribute_name
                for i in range(len(self.function_nodes)):
                    ans += ')'
            # if len(self.value_nodes) > 0:
            #     if ans != '':
            #         ans = 'SELECT ' + ans + ' WHERE'
            #     else:
            #         ans = 'SELECT ' + self.attribute_name + ' WHERE'
            #     for vn in self.value_nodes:
            #         ans += ' '
            #         ans += str(vn).replace('.', '=')
        return ans

    def __repr__(self):
        self.__str__()


class Target(object):
    def __init__(self, _attribute, _type):
        self.attribute = _attribute
        self.type = _type

    def __str__(self):
        if self.type is not None:
            return self.type + '(' + self.attribute + ')'
        else:
            return self.attribute

    def __repr__(self):
        return self.__str__()


class ConditionBlock(object):
    """
    value can be a value or another ConditionBlock
    """

    def __init__(self, an=None, op=None, value=None):
        self.an = an
        self.op = op
        self.value = value
        # 默认情况下与下一个条件块用AND 逻辑连接
        self.relation_with_next = 'AND'

    def __repr__(self):
        return "condition block ==> " + \
               str(self.an) + ' ' + str(self.op) + " " + str(self.value) + " " + self.relation_with_next

    def change_relation_to_or(self):
        """
        将和下一个ConditionBlock的连接关系改为OR
        :return:
        """
        self.relation_with_next = 'OR'

    def __str__(self):
        return self.__repr__()

    def to_string(self):
        return str(self.an) + ' ' + str(self.op) + " " + str(self.value)