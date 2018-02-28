"""
   parser warp the database info, sentence, semantic nodes together

"""

from ch2sql.tools.hit_ltp import LtpParser
import re
from ch2sql.tools.exception import *


class Target(object):
    def __init__(self, _attribute, _type):
        self.attribute = _attribute
        self.type = _type

    def __str__(self):
        if self.type is not None:
            return self.type + '(' + self.attribute + ')'
        else:
            return 'AN: ' + self.attribute

    def __repr__(self):
        return self.__str__()


class AN(object):
    """

     将 Attribute Node 单独提取出来
     目的是将 聚集函数, Group by 等描述属性节点的节点合并到AN中
     使之成为一个整体

    """

    def __init__(self, _a, _t):
        self.attribute_name = _a
        self.attribute_type = _t
        self.group_by = False
        self.function_node = []
        self.top_node = None
        self.nodes_index = []

    def add_group_by_node(self):
        self.group_by = True

    def add_function_node(self, f):
        self.function_node.append(f)

    def add_top_node(self, top_value):
        self.top_node = top_value

    def add_nodes_index(self, index):
        self.nodes_index.append(index)

    def sort_function_nodes(self):
        """
        function node 不止一个的时候需要对这些nodes进行排序
        :return:
        """
        pass

    def __str__(self):
        self.sort_function_nodes()
        ans = ''
        print(self.function_node)
        if len(self.function_node) > 0:
            for f in self.function_node:
                ans = ans + str(f) + '('
            ans += self.attribute_name
            for i in range(len(self.function_node)):
                ans += ')'
        return ans

    def __repr__(self):
        self.__str__()


class ConditionBlock(object):
    """
    value can be a value or another ConditionBlock
    """

    def __init__(self, an=None, op=None, value=None):
        self.an = an
        self.op = op
        self.value = value

    def __repr__(self):
        return "condition block ==> " + \
               str(self.an) + ' ' + str(self.op) + " " + str(self.value)

    def __str__(self):
        return self.__repr__()


class Parser(object):
    """
    init by a Sentence object
    build a database semantic related parse tree
    thus to generate condition blocks and target blocks for this
    natural language query.
    """

    def __init__(self, sentence):
        self.sentence = sentence
        self._table = self.sentence.table
        self.nodes = self.sentence.nodes
        self.remove_meaningless_nodes()
        self.tokens = self.sentence.tokens
        self.targets = []
        self.conditions = []
        self.condition_sentence = None

    def remove_meaningless_nodes(self):
        """
        remove the nodes with 'UN' types(Unknown Node)
        :return: list: removed_nodes
        """
        removed_nodes = []
        for node in self.nodes:
            if node.nodeInfo.type == 'UN':
                self.nodes.remove(node)
                removed_nodes.append(node)
        return removed_nodes

    def top_parser(self):
        pass

    def sort_parser(self):
        pass

    def select_parser(self):
        """
        to get the targets in a query sentence(after 'SELECT')
        every target is wrapped by a Target object
        :return: list of Targets
        """
        self.remove_meaningless_nodes()
        result = []
        # FA: function node  & attribute node eg.'平均销售量'
        # AF: attribute node & function node eg.'销售量最大值'
        # A: attribute node eg.'销售量'
        target_modes = ['FA', 'AF', 'A', 'F']
        nodes = list(self.nodes)
        tokens = list(self.tokens)

        def _target_find():
            for mode in target_modes:
                for i in range(len(tokens) - 1, -1, -1):
                    node_type_list = []
                    node_list = []
                    j = i
                    while j <= len(nodes) - 1:
                        node_type_list.append(nodes[j].nodeInfo.type)
                        node_list.append(nodes[j])
                        j += 1
                    if len(node_type_list) == len(mode):
                        tag = ''
                        for t in node_type_list:
                            tag += t[0]
                        if tag == mode:
                            if mode == 'FA':
                                result.append(Target(_attribute=node_list[1].nodeInfo.symbol,
                                                     _type=node_list[0].nodeInfo.symbol))
                            elif mode == 'AF':
                                result.append(Target(_attribute=node_list[0].nodeInfo.symbol,
                                                     _type=node_list[1].nodeInfo.symbol))
                            elif mode == 'A':
                                result.append(Target(_attribute=node_list[0].nodeInfo.symbol,
                                                     _type=None))
                            elif mode == 'F':
                                if node_list[0].nodeInfo.symbol == 'COUNT':
                                    result.append(Target(_attribute='COUNT(*)', _type=None))
                                else:
                                    raise IllegalQueryException("查询结果不能是count以外的其他函数!")

                            # 将匹配的结果切除
                            size_to_drop = len(mode)
                            while size_to_drop > 0:
                                nodes.remove(nodes[-1])
                                tokens.remove(tokens[-1])
                                size_to_drop -= 1
                            # 切除以后的末尾是连词或者逗号,此时应该继续匹配
                            # 这里使用递归的方法反复匹配
                            if len(nodes) > 0 and \
                                    (nodes[-1].nodeInfo.symbol == 'AND' or nodes[-1].pos_tag == 'wp'):
                                # 切除连词
                                nodes.remove(nodes[-1])
                                _target_find()
                            # 否则结束调用 函数返回
                            else:
                                return
                    elif len(node_type_list) > len(mode):
                        break

        _target_find()
        if len(result) == 0:
            result.append(Target(_attribute='ALL', _type=None))
        # 将nodes替换为切分以后的nodes, 处理后的nodes只剩下条件块
        self.nodes = nodes
        self.tokens = tokens
        return result

    def condition_parser(self):
        """
        process with the condition sentence
        :return:
        """
        # 切除句首的SN eg. '查询','看看' 一类的动词
        nodes = self.nodes
        tokens = [nodes[i].word for i in range(len(nodes))]
        if len(nodes) > 0 and nodes[0].nodeInfo.type == 'SN':
            nodes.remove(nodes[0])
            tokens.remove(tokens[0])
        pos_tag = [nodes[i].pos_tag for i in range(len(nodes))]
        condition_arcs = LtpParser.dependency_parsing(tokens, pos_tag)
        arcs = condition_arcs
        for item in list(arcs):
            print("{} {}".format(item.head, item.relation))

        def find_relations_by_head(head_id):
            _result = []
            for i in range(len(arcs)):
                if arcs[i].head == head_id:
                    _result.append(i)
            return _result

        def find_nodes_by_type(node_type):
            _index = []
            for i in range(len(nodes)):
                if nodes[i].nodeInfo.type == node_type:
                    _index.append(i)
            return _index

        def connect_nodes_to_an(an_, an_index_):
            """
            找出attribute node的联系节点. 聚集函数节点(FN), group by 节点(GN), top 节点(TN)等
            必须和attribute node 节点联系在一起才有意义
            :param an_:
            :param an_index_:
            :return:
            """
            attribute_name = an_.nodeInfo.symbol
            d_type = self._table.get_column_type_by_name(attribute_name)
            an_tmp = AN(attribute_name, d_type)
            relation_index_ = find_relations_by_head(an_index_ + 1)

            for _r in relation_index_:
                if arcs[_r].relation == 'ATT':
                    # Group By 节点
                    if nodes[_r].nodeInfo.type == 'GN':
                        an_tmp.group_by = True
                        an_tmp.add_nodes_index(_r)
                    # Function node
                    elif nodes[_r].nodeInfo.type == 'FN':
                        an_tmp.add_function_node(nodes[_r].nodeInfo.symbol)
                        an_tmp.add_nodes_index(_r)

            # 寻找top node
            # 例 "平均销售量top10", '下载量top10' 等
            for i_ in range(len(nodes)):
                if nodes[i_].nodeInfo.type == 'TN':
                    relation_index_ = find_relations_by_head(head_id=i_ + 1)
                    for _r in relation_index_:
                        # 如果top node ATT 依赖是此函数中考虑的an_节点
                        # 则top节点修饰这个an_节点
                        if _r == an_index_ and arcs[_r].relation == 'ATT':
                            an_tmp.add_top_node(int(nodes[an_index_].nodeInfo.symbol))
                            an_tmp.add_nodes_index(i_)

            an_tmp.add_nodes_index(an_index_)
            return an_tmp

        # tackle with 'attribute op value' mode, like '年齡大于20' etc
        # 暂时不支持递归查询(通过是否含有 操作符节点[ON]识别)
        on_nodes = find_nodes_by_type('ON')
        if len(on_nodes) > 0:
            for index in on_nodes:
                head = index + 1
                relation_index = find_relations_by_head(head_id=head)
                condition_block = ConditionBlock()
                op = nodes[index].nodeInfo.symbol
                op_ = nodes[index]
                an = None
                val = None
                an_index = 0
                for r in relation_index:
                    if arcs[r].relation == 'SBV':
                        an = nodes[r]
                        an_index = r
                    elif arcs[r].relation == 'VOB':
                        val = nodes[r]
                        val_index = r

                # 如果an 的type是'AN', 则将an包装为AN class 类型数据
                if an is not None and an.nodeInfo.type == 'AN':
                    an = connect_nodes_to_an(an, an_index)

                # VN 的value是 '表名.属性'的形式,用正则将二者分离
                regex = re.compile(r'(\w+)\.(\w+)')

                if an is not None and type(an) == AN:
                    # 获取节点对应的数据列的数据类型
                    data_type = an.attribute_type
                    if val is not None and val.nodeInfo.type == 'AN':
                        if data_type != self._table.get_column_type_by_name(
                                val.nodeInfo.symbol
                        ):
                            raise IllegalQueryException('>>>条件与值类型不匹配')
                        if op.nodeInfo.type == '=':
                            pass

                    elif val is not None and val.nodeInfo.type == 'VN':
                        tmp = re.findall(regex, val.nodeInfo.symbol)
                        val.nodeInfo.symbol = tmp[0][1]
                        attribute = tmp[0][0]
                        if attribute != an.attribute_name:
                            pass
                        condition_block.value = val

                    elif val is not None and val.nodeInfo.type == 'NUMBER':
                        if data_type != 'number':
                            raise IllegalQueryException('>>>属性不是数值类型')
                        else:
                            condition_block.value = val
                    elif val is not None and val.nodeInfo.type == 'DATE':
                        if data_type != 'date':
                            raise IllegalQueryException('>>>属性不是日期类型')
                        else:
                            condition_block.value = val
                    else:
                        condition_block.value = val

                # 主语缺失
                else:
                    raise IllegalQueryException('>>>条件主语缺失')
                condition_block.an = an
                condition_block.op = op
                self.conditions.append(condition_block)
                print(condition_block)

                # 清除在此轮中匹配的节点
                nodes_index_to_clean = an.nodes_index.copy()
                nodes_index_to_clean.append(nodes.index(val))
                nodes_index_to_clean.append(nodes.index(op_))
                for node_tmp in nodes_index_to_clean:
                    nodes.remove(node_tmp)

        # 纯粹值节点情况处理
        # 如'武汉天气' 其中的'武汉' 标准的说法应该是: 地区是武汉
        value_nodes = find_nodes_by_type('VN')
        if len(value_nodes) == 1:
            pass

    def from_parser(self):
        return self._table.table_name

    def drop_node(self):
        pass


if __name__ == "__main__":
    pass
