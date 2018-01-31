# -*-coding:utf-8 -*-


class NodeInfo(object):
    """
    表示节点的信息, 如 word="大于" type="ON"(操作符节点) symbol='>'
    如果type='NN' 或者type='VN', 则score表示节点属于这个类型的概率得分值
    """

    def __init__(self, _word, _type, _symbol, _score=None):
        self.word = _word
        self.type = _type
        self.symbol = _symbol
        self.score = _score

    def __str__(self):
        return "word:{} type:{} symbol:{} score:{}".format(self.word, self.type, self.symbol, self.score)

    def __repr__(self):
        return "word:{} type:{} symbol:{} score:{}".format(self.word, self.type, self.symbol, self.score)


class NodeMapper(object):
    node_map = dict()
    # Select Node
    node_map['查询'] = NodeInfo('查询', 'SN', 'SELECT')
    node_map['看看'] = NodeInfo('看看', 'SN', 'SELECT')
    node_map['返回'] = NodeInfo('返回', 'SN', 'SELECT')
    # node type hard code part...¬
    # Operator Node
    # TODO 用正则表达式处理中文中常常出现的'比...高模式'
    node_map['大于'] = NodeInfo('大于', 'ON', '>')
    node_map['高于'] = NodeInfo('高于', 'ON', '>')
    node_map['小于'] = NodeInfo('大于', 'ON', '>')
    node_map['低于'] = NodeInfo('低于', 'ON', '>')
    node_map['相当于'] = NodeInfo('相当于', 'ON', '=')
    node_map['等于'] = NodeInfo('等于', 'ON', '=')
    node_map['是'] = NodeInfo('是', 'ON', '>')

    # Function Node
    node_map['平均'] = NodeInfo('平均', 'FN', 'AVG')
    node_map['平均值'] = NodeInfo('平均值', 'FN', 'AVG')
    node_map['最大'] = NodeInfo('最大', 'FN', 'MAX')
    node_map['最高'] = NodeInfo('最高', 'FN', 'MAX')
    node_map['最小'] = NodeInfo('最小', 'FN', 'MIN')
    node_map['最低'] = NodeInfo('最低', 'FN', 'MIN')
    node_map['总数'] = NodeInfo('总数', 'FN', 'SUM')
    node_map['总量'] = NodeInfo('总量', 'FN', 'SUM')
    node_map['之和'] = NodeInfo('之和', 'FN', 'SUM')
    node_map['总数'] = NodeInfo('总数', 'FN', 'COUNT')

    # Quantifier Node
    node_map['所有'] = NodeInfo('所有', 'QN', 'ALL')
    node_map['全部'] = NodeInfo('全部', 'QN', 'ALL')
    node_map['任意'] = NodeInfo('任意', 'QN', 'ANY')

    # ...

    @staticmethod
    def get_possible_node_info_list(node, table):
        from ch2sql.tools import similar
        result = []
        word = node.word
        # hard code node
        if word in NodeMapper.node_map:
            result.append(NodeMapper.node_map[word])
            return result
        for column_name in table.get_column_names():
            score = similar.similar_scores(column_name, word)
            result.append(NodeInfo(word, 'AN', column_name, _score=score))
            # 只有对column数据类型是text才抽样取值
            if table.get_column_by_name(column_name).data_type != "text":
                continue
            # 最多只取到200个值
            values = table.get_values_set_by_name(name=column_name, num=200)
            for value in values:
                if value is None or type(value) != str or len(value) == 0:
                    continue
                score = similar.similar_scores(word, value)
                result.append(NodeInfo(word, 'NN', column_name + '.' + value, _score=score))
        return result


class Node(object):
    """
       基于数据库语义的节点表示类
       fields:
           str: initWord: 原始单词
           str: stdWord: 数据库语义的标准词
           str: posTag: 词性标注类型
           str: dataType 数据类型(text, date, number)  如果nodeType是AN, 或者NN
           str: nodeType 节点类型,我们将节点划分为8个类型
                SE  Select Node 选择节点("返回","看看","查询" 等查询动词)
                ON  Operator Node 操作符节点("等于","大于","包含","不等于" 等)
                FN  Function Node 聚集函数节点("之和","最大","最低","平均" 等)
                AN  Attribute Node 属性节点(非硬编码, 对应数据表的属性名,从table或者tableName.sql中自动获取)
                VN  Value Node 值节点(非硬编码, 属性节点对应的值)
                LN  Logical Node 逻辑节点(和 ',' '且')
                GN Group Node 分组节点('各','各个','每个'等, 对应SQL中的GROUP BY)
                QN Quantifier Node  数量节点('任意','全部')
                SN Sort Node 排序节点('从高到低','按照顺序显示')
                TN Top Node ("top100", "前10个")
                UN Unknown Node 未知类型节点
           Node parent
           list: Node child
    """

    def __init__(self, word, table, pos_tag):
        self.word = word
        self.table = table
        self.pos_tag = pos_tag
