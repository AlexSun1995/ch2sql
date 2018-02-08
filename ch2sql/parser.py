"""
   parser warp the database info, sentence, semantic nodes together

"""

from ch2sql.tools.hit_ltp import LtpParser


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


class Parser(object):
    """
    init by a Sentence object
    build a database semantic related parse tree
    thus to generate condition blocks and target blocks for this
    natural language query.
    """
    parser = LtpParser

    def __init__(self, sentence):
        self.sentence = sentence
        self._table = self.sentence.table
        self.targets = []
        self.condition_sentence = None

    def get_targets(self):
        """
        to get the targets in a query sentence(after 'SELECT')
        every target is wrapped by a Target object
        :return: list of Targets
        """
        result = []
        # FA: function node  & attribute node eg.'平均销售量'
        # AF: attribute node & function node eg.'销售量最大值'
        # A: attribute node eg.'销售量'
        target_modes = ['FA', 'AF', 'A']
        nodes = list(self.sentence.nodes)
        tokens = list(self.sentence.tokens)

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
                    elif len(node_type_list) > len(mode):
                        break

        _target_find()
        if len(result) == 0:
            result.append(Target(_attribute='ALL', _type=None))
        return result

    def drop_node(self):
        pass

    def get_condition_sentence(self):
        """
        to get the condition sentence in a query
        :return:
        """
        pass


class SetBlock(object):
    pass


if __name__ == "__main__":
    # test.input_processing("比北京大")
    pass
