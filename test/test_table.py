import pytest


def setup_module(test_table):
    print("start, module name {}".format(test_table.__name__))


def test_excel():
    print("test excel 01")
    from ch2sql.tools.excel import ExcelWrapper
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    excel = ExcelWrapper(path)
    assert excel.length == 14
    assert (len(excel.title_values['APP下载量']) == len(excel.title_values['点击量']))
    assert excel.title_type_dict['APP下载量'] == 'number'
    print(excel.title_type_dict['日期'])
    assert excel.title_type_dict['日期'] == 'date'


def test_table():
    print("test excel 01")
    from ch2sql.database import Table
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    print(path)
    table = Table(table_name='广告投放效果', path=path)
    # print(list(table.column_names()))
    assert len((list(table.get_column_names()))) > 0
    # test column 属性名
    li = []
    li_2 = []
    for col in table:
        li.append(col.name)
        li_2.append(col.data_type)
    print(li)
    print(li_2)
    assert len(li) == len(li_2)
    # test column 属性值
    assert table.columns is not None
    print(table.get_column_by_index(2).data_type)


def test_jieba_cut():
    # 这里测试保证数据表的title关键词不能被分词工具拆开
    # 如"APP下载量" 不能被拆成"APP", "下载量"
    # 1.31 2:12 am 测试通过
    print("test jieba cut funtion")
    from ch2sql.database import Table
    from ch2sql.sentence import Sentence
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='广告投放效果', path=path)
    s1 = "APP下载量"
    s2 = "独立访问用户"
    s1 = Sentence(s1, table)
    s2 = Sentence(s2, table)
    assert (len(s1.tokens) == len(s2.tokens) == 1)


def test_ltp():
    """
    对LtpParser 类进行测试
    :return:
    """
    from ch2sql.tools.hit_ltp import LtpParser
    from ch2sql.database import Table
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='广告投放效果', path=path)
    ltp = LtpParser()
    s = "下载量比APP激活量大"
    tokens = LtpParser.cutting(s, table)
    tags = LtpParser.pos_tagging(tokens)
    entities = LtpParser.entity_recognize(tokens, tags)
    arcs = LtpParser.dependency_parsing(tokens, tags)
    print(list(entities))
    print("\t".join("%s -- > %s:%s; " % (tokens[arcs[i].head - 1], tokens[i], arcs[i].relation)
                    for i in range(len(arcs))))


def test_sentence():
    """
    Sentence对输入的查询语句进行了包装, 依赖于LtpParse类进行自然语言处理
    :return:
    """
    # 1.31 3:44 PM 测试通过
    from ch2sql.database import Table
    from ch2sql.sentence import Sentence
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='广告投放效果', path=path)
    s1 = "APP下载量在10万和12万之间的数据"
    s1 = Sentence(s1, table)
    print(s1.tokens)
    print(list(s1.pos_tags))
    print(s1.dp_tree)


def test_mapping():
    from ch2sql.database import Table
    from ch2sql.sentence import Sentence
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "看看税费Top10的数据"
    s1 = Sentence(s1, table)
    s1.node_mapping()
    print(s1.print_nodes())
    print(s1.dp_tree)


def test_stopwords():
    from ch2sql.tools import similar
    assert similar.is_stopwords("等于") is False
    assert similar.is_stopwords("的") is True


def test_sentence2():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='广告投放效果', path=path)
    s1 = "查询APP下载量比APP激活量大的数据"
    s1 = Sentence(s1, table)
    print(s1.sentence)
    s1.node_mapping()
    tokens = s1.tokens
    arcs = s1.dp_tree
    print("\t".join("%s -- > %s:%s; " % (tokens[arcs[i].head - 1], tokens[i], arcs[i].relation)
                    for i in range(len(arcs))))
