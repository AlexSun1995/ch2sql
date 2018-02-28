def test_target_get():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='广告投放效果', path=path)
    # s1 = "查询最大APP下载量"
    # s1 = Sentence(s1, table)
    # print(s1.nodes)
    # from ch2sql.parser import Parser
    # s1 = Parser(s1)
    # res = s1.select_parser()
    # print(res)  # [MAX(APP下载量)] 结果正确

    # s2 = "查询最大APP下载量和平均APP下载量"
    # s2 = Sentence(s2, table)
    # print(s2.nodes)
    # from ch2sql.parser import Parser
    # s2 = Parser(s2)
    # res = s2.select_parser()
    # print(res)  # [AVG(APP下载量), MAX(APP下载量)] 结果正确

    s3 = "查询今年每个月的APP下载量总量和平均APP激活量"
    s3 = Sentence(s3, table)
    print(s3.nodes)
    from ch2sql.parser import Parser
    s2 = Parser(s3)
    res = s2.select_parser()
    print(res)  # [AVG(APP下载量), MAX(APP下载量)] 结果正确


def test_condition_parser1():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询最高平均不含税金额大于1000的数据"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    print(s1.select_parser())
    s1.condition_parser()
    # 测试结果
    # condition block ==> MAX(AVG(不含税金额)) > <word:1000 type:NUMBER symbol:1000>


def test_condition_parser2():
    """
    测试值条件节点的处理情况
    eg: "京东商城的最高单价"
    :return:
    """
    pass
