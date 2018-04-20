"""
   parser warp the database info, sentence, semantic nodes together
   author Alex Sun

"""

from ch2sql.tools.hit_ltp import LtpParser
from ch2sql.tools.exception import *
from ch2sql.parser_unit import *


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
        self.group_by_attribute = []
        self.select_targets = None
        self.parser_tree = None
        # eg.销量top10, ("销量", 10)
        self.top_attribute_and_number = []
        self.date_from = None
        self.date_to = None
        self.time_parser(self.sentence.init_sentence)

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

    def group_by_parser(self):
        pass

    def time_parser(self, str_in):
        """
        抽取查询语句中的时间信息
        :return:
        """
        from ch2sql.date_pro import ch2date
        try:
            begin, end, isRange, byMon, byYear, isError = ch2date(str_in)
            if not isRange:
                self.date_from = begin
                self.date_to = begin
            else:
                self.date_from = begin
                self.date_to = end
        except BaseException:
            print("时间抽取失败")

    def sort_parser(self):
        # TODO
        pass

    def select_parser(self):
        """
        to get the targets in a query sentence(after 'SELECT')
        every target is wrapped by a Target object
        :return: list of Targets
        """
        # self.remove_meaningless_nodes()
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
                                    raise IllegalQueryException("不能是count以外的其他函数!")

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
        self.select_targets = result
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
        self.parser_tree = condition_arcs
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
            找出attribute node的联系节点. 聚集函数节点(FN), group by 节点(GN), top 节点(TN)
            以及值节点(value node)等
            必须和attribute node 节点联系在一起才有意义
            :param an_:
            :param an_index_:
            :return:
            """
            attribute_name = an_.nodeInfo.symbol
            d_type = self._table.get_column_type_by_name(attribute_name)
            an_tmp = ExpandAN(an_, d_type)
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
                    # Top Node
                    elif nodes[_r].nodeInfo.type == 'TN':
                        an_tmp.add_top_node(nodes[_r].nodeInfo.symbol)
                        an_tmp.add_nodes_index(_r)
                    # Value Node
                    elif nodes[_r].nodeInfo.type == 'VN':
                        an_tmp.add_value_nodes(nodes[_r].nodeInfo.symbol)
                        # an_tmp.add_nodes_index(_r)

            # 寻找top node
            # 例 "平均销售量top10", '下载量top10' 等
            for i_ in range(len(nodes)):
                if nodes[i_].nodeInfo.type == 'TN':
                    relation_index_ = find_relations_by_head(head_id=i_ + 1)
                    for _r in relation_index_:
                        # 如果top node ATT 依赖是此函数中考虑的an_节点
                        # 则top节点修饰这个an_节点
                        if _r == an_index_ and arcs[_r].relation == 'ATT':
                            an_tmp.add_top_node(int(nodes[i_].nodeInfo.symbol))
                            an_tmp.add_nodes_index(i_)

            an_tmp.add_nodes_index(an_index_)
            return an_tmp

        # tackle with 'attribute op value' mode, like '年齡大于20' etc
        # 暂时不支持递归查询(通过是否含有操作符节点[ON]识别)
        expand_an = None
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
                an_index = -1
                val_index = -1
                for r in relation_index:
                    if arcs[r].relation == 'SBV':
                        an = nodes[r]
                        an_index = r
                    elif arcs[r].relation == 'VOB':
                        val = nodes[r]
                        val_index = r

                # expand_val_an = None
                # 如果an 的type是'AN', 则将an包装为ExpandAN class 类型数据
                if an is not None and an.nodeInfo.type == 'AN':
                    expand_an = connect_nodes_to_an(an, an_index)

                # 如果val的type是'AN', 则将val包装为ExpandAN class类型的数据
                if val is not None and val.nodeInfo.type == 'AN':
                    expand_val_an = connect_nodes_to_an(val, val_index)
                    if expand_an is not None:
                        data_type = expand_an.attribute_type
                        if expand_val_an is not None:
                            if data_type != self._table.get_column_type_by_name(
                                    val.nodeInfo.symbol
                            ):
                                raise IllegalQueryException('>>>条件与值类型不匹配')
                            if op.nodeInfo.type == '=':
                                pass
                    else:
                        raise IllegalQueryException('>>>expand_an is None')
                    condition_block.an = an
                    condition_block.op = op
                    condition_block.value = expand_val_an.attribute_name
                elif val is not None and val.nodeInfo.type == 'VN':
                    # VN 的value是 '表名.属性'的形式,用正则将二者分离
                    regex = re.compile(r'(\w+)\.(\w+)')
                    if expand_an is not None:
                        tmp = re.findall(regex, val.nodeInfo.symbol)
                        val.nodeInfo.symbol = tmp[0][1]
                        attribute = tmp[0][0]
                        if attribute != an.attribute_name:
                            raise IllegalQueryException("值类型与属性类型不匹配")
                        if op.nodeInfo.type != '=':
                            raise IllegalQueryException("比较符号只能是='")
                        condition_block.an = expand_an.attribute_name
                        condition_block.op = '='
                        condition_block.value = val
                    else:
                        raise IllegalQueryException("缺少属性节点")

                elif val is not None and val.nodeInfo.type == 'NUMBER':
                    if expand_an is not None:
                        an_data_type = expand_an.attribute_type
                        if an_data_type != 'number':
                            raise IllegalQueryException("属性数据类型应该是数值型的")
                        condition_block.op = op
                        condition_block.an = expand_an.attribute_name
                        condition_block.value = val.nodeInfo.symbol
                    else:
                        raise IllegalQueryException("缺少属性节点")

                elif val is not None and val.nodeInfo.type == 'DATE':
                    if expand_an is not None:
                        an_data_type = expand_an.attribute_type
                        if an_data_type != 'date':
                            raise IllegalQueryException("属性数据类型应该是date型的")
                        condition_block.op = op
                        condition_block.an = expand_an.attribute_name
                        condition_block.value = val.nodeInfo.symbol

                self.conditions.append(condition_block)
                # 清除在此轮中匹配的节点
                nodes_index_to_clean = expand_an.nodes_index.copy()
                nodes_index_to_clean.append(nodes.index(val))
                nodes_index_to_clean.append(nodes.index(op_))
                nodes_index_to_clean = sorted(nodes_index_to_clean, reverse=True)
                for node_tmp in nodes_index_to_clean:
                    print(node_tmp)
                    nodes.remove(nodes[node_tmp])

        # 纯粹值节点情况处理
        # 如'武汉天气' 其中的'武汉' 标准的说法应该是: 地区是武汉,
        # 提取出值节点(VN), 并将其标准化. 如果有多个VN, 默认情况下用AND进行逻辑连接
        value_nodes = find_nodes_by_type('VN')
        regex = re.compile(r'(\w+)\.(\w+)')
        if len(value_nodes) == 1:
            val_node = nodes[value_nodes[0]]
            tmp = re.findall(regex, val_node.nodeInfo.symbol)
            value = tmp[0][1]
            attribute = tmp[0][0]
            op = '='
            value_condition = ConditionBlock(attribute, op, value)
            self.conditions.append(value_condition)

        elif len(value_nodes) > 1:
            value_conditions = []
            for i in range(len(value_nodes)):
                val_node = nodes[value_nodes[i]]
                tmp = re.findall(regex, val_node.nodeInfo.symbol)
                value = tmp[0][1]
                attribute = tmp[0][0]
                op = '='
                value_condition = ConditionBlock(attribute, op, value)
                value_conditions.append(value_condition)

                # 如果i>0, 在value_nodes[i-1] 和value_nodes[i]
                # 之间找有没有值为'OR'的逻辑节点
                if i > 0:
                    left_index = nodes.index(nodes[value_nodes[i - 1]])
                    right_index = nodes.index(nodes[value_nodes[i]])
                    for p in range(left_index + 1, right_index):
                        if nodes[p].nodeInfo.symbol == 'OR':
                            value_conditions[len(value_conditions) - 2].change_relation_to_or()

            # 将value_conditions中的数据放进self.conditions 中
            for c in value_conditions:
                self.conditions.append(c)

        # 如果nodes中还存在AN节点, 则可能是top节点或者group_by节点修饰的AN
        an_nodes = find_nodes_by_type('AN')
        if len(an_nodes) == 1:
            cur_an_index = an_nodes[0]
            an0 = connect_nodes_to_an(nodes[cur_an_index], cur_an_index)
            if an0.group_by:
                self.group_by_attribute.append(nodes[cur_an_index].nodeInfo.symbol)

            if an0.top_node is not None:
                self.top_attribute_and_number.append((an0.attribute_name, an0.top_node))

            if len(an0.function_nodes) > 0:
                tmp_c = ConditionBlock()
                tmp_c.an = an0.attribute_name
                tmp_c.op = "="
                tmp_c.value = str(an0)
                self.conditions.append(tmp_c)

        elif len(an_nodes) > 1:
            raise IllegalQueryException("属性节点太多!")

        print("group_by attribute")
        print(self.group_by_attribute)
        print("-----> top attribute")
        print(self.top_attribute_and_number)
        print(self.conditions)

    def from_parser(self):
        return self._table.table_name


if __name__ == "__main__":
    pass
