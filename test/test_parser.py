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
    # res = s1.get_targets()
    # print(res)  # [MAX(APP下载量)] 结果正确

    # s2 = "查询最大APP下载量和平均APP下载量"
    # s2 = Sentence(s2, table)
    # print(s2.nodes)
    # from ch2sql.parser import Parser
    # s2 = Parser(s2)
    # res = s2.get_targets()
    # print(res)  # [AVG(APP下载量), MAX(APP下载量)] 结果正确

    s3 = "查询最大APP下载量和平均APP下载量"
    s3 = Sentence(s3, table)
    print(s3.nodes)
    from ch2sql.parser import Parser
    s2 = Parser(s3)
    res = s2.get_targets()
    print(res)  # [AVG(APP下载量), MAX(APP下载量)] 结果正确