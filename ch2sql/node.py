# -*-coding:utf-8 -*-

class NodeInfo(object):
    pass


class Node(object):
    """
       基于数据库语义的节点表示类
       fields:
           str: initWord: 原始单词
           str: stdWord: 数据库语义的标准词
           str: posTag: 词性标注类型
           str: dataType 数据类型(text, date, number)  如果nodeType是AN
           str: nodeType 节点类型,我们将节点划分为8个类型
                SE  Select Node 选择节点("返回","看看","查询" 等查询动词)
                ON  Operator Node 操作符节点("等于","大于","包含","不等于" 等)
                FN  Function Node 聚集函数节点("之和","最大","最低","平均" 等)
                AN  Attribute Node 属性节点(非硬编码, 对应数据表的属性名,从table或者tableName.sql中自动获取)
                VN  Value Node 值节点(非硬编码, 属性节点对应的值)
                LN  Logical Node 逻辑节点(和 ',' '且')
                GN Group Node 分组节点('各','各个','每个'等, 对应SQL中的GROUP BY)
                QN Quantifier Node  数量节点('任意','全部','前10','top100' 等)
                SN Sort Node 排序节点('从高到低','按照顺序显示')
                UN Unknown Node 未知类型节点
           Node parent
           list: Node child
    """
    pass


if __name__ == "__main__":
    pass
