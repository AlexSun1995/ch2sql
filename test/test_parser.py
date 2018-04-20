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
    eg: "京东商城的平均单价"
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "京东商城的平均单价"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    print(s1.select_parser())
    s1.condition_parser()


def test_condition_parser3():
    """
    带有逻辑连接符号的纯值条件节点解析
    eg. '销售部或者电子商务部'
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "销售部或者电子商务部的情况"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.condition_parser()
    # 运行结果
    # [condition block ==> 部门名称 = 销售部 OR, condition block ==> 部门名称 = 电子商务 AND]


def test_condition_parser4():
    """
    对包含group by top修饰的属性名条件节点解析
    eg. "各部门的平均税费"
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各部门名称的平均税款"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    print(s1.select_targets)
    s1.condition_parser()


def test_condition_parser5():
    """
    top
    eg. "利润top10的部门名称"
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "利润top10的部门名称"
    s1 = Sentence(s1, table)
    print("nodes---->")
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    print(s1.select_targets)


def test_condition_parser6():
    """
    top
    eg. "利润top10的部门名称"
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "不同部门名称的利润均值"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    print(s1.select_targets)
    print(s1.conditions)


def test_total_01():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "京东商城税费小于10的单据日期"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    print(s1.select_targets)
    print(s1.conditions)


def test_total_02():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "北京上海两地的情况"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_03():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "利润top100"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_04():
    """
    {
    "select": [
        "订单号"
    ],
    "condition_and": [
        "客户名称 = 京东商城"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询京东商城的订单编号"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_05():
    """
    {
    "select": [
        "SUM(订单号)"
    ],
    "condition_and": [
        "客户名称 = 京东商城"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询京东商城的总订单额"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_06():
    """
    {
    "select": [
        "客户编码"
    ],
    "condition_and": [
        "部门名称 = 电子商务"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询客户分类为电子商务的客户名和客户编码"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_07():
    """
    {
    "select": [
        "SUM(订单金额)",
        "业务员姓名"
    ],
    "condition_and": [],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [
        "业务员姓名"
    ],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
     }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各业务员姓名的总订单金额"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_08():
    """
     在这种情况下会出现混乱
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各业务员的总订单金额"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_09():
    """
    {
    "select": [
        "客户名称",
        "利润"
    ],
    "condition_and": [],
    "condition_or": [],
    "order_by_desc": [
        "利润"
    ],
    "group_by": [],
    "having": [],
    "result_limit": 10,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "利润top10的客户名称"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_10():
    """
    {
    "select": [
        "存货名称"
    ],
    "condition_and": [
        "数量 > 100",
        "客户名称 = 京东商城"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询京东商城销量大于100的存货名称"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_11():
    """
    {
    "select": [
        "客户名称"
    ],
    "condition_and": [
        "税费 = MIN(税费)"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "查询最少税费客户名称"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_12():
    """
    {
    "select": [
        "AVG(税费)",
        "部门名称"
    ],
    "condition_and": [],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [
        "部门名称"
    ],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各部门名称的平均税款"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_13():
    """
    {
    "select": [
        "COUNT(订单号)",
        "部门名称"
    ],
    "condition_and": [],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [
        "部门名称"
    ],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各部门名称的订单号总数"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_14():
    """
    {
    "select": [
        "ALL"
    ],
    "condition_and": [
        "地区名称 = 北京"
    ],
    "condition_or": [
        "地区名称 = 上海"
    ],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "data_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "北京或者上海的销售情况"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_15():
    """
    {
    "select": [
        "存货分类"
    ],
    "condition_and": [
        "客户名称 = 大地电子科技公司"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": null,
    "date_to": null
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "大地电子科技公司的存货分类"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_16():
    """
    {
    "select": [
        "客户名称"
    ],
    "condition_and": [
        "订单号 > 50"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": "None",
    "date_to": "None"
    }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "订单号大于50的客户名称"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_17():
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "订单编号大于50的客户名称"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_18():
    """
    {
    "select": [
        "单据日期"
    ],
    "condition_and": [
        "税费 < 10",
        "客户名称 = 京东商城"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": "None",
    "date_to": "None"
     }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "京东商城税费小于10的单据日期"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    print(s1.parser_tree)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_19():
    """
    {
    "select": [
        "COUNT(订单号)",
        "部门名称"
    ],
    "condition_and": [],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [
        "部门名称"
    ],
    "having": [],
    "result_limit": null,
    "date_from": "None",
    "date_to": "None"
   }
    :return:
    """
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = "各部门名称的订单号总数"
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    print(s1.parser_tree)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_20():
    """
    {
    "select": [
        "利润"
    ],
    "condition_and": [
        "客户名称 = 淘宝网"
    ],
    "condition_or": [],
    "order_by_desc": [],
    "group_by": [],
    "having": [],
    "result_limit": null,
    "date_from": "2014-12-01",
    "date_to": "2014-12-31"
     }
    :return:
    """

    s1 = "2014年12月淘宝网的利润"
    from ch2sql.sentence import Sentence
    from ch2sql.database import Table
    from ch2sql.parser import Parser
    import os
    path = "../datasource/销售业绩报表.xlsx"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    table = Table(table_name='销售业绩报表', path=path)
    s1 = Sentence(s1, table)
    print(s1.nodes)
    s1 = Parser(s1)
    print(s1.parser_tree)
    s1.select_parser()
    s1.condition_parser()
    from ch2sql.output import Output
    o = Output(s1)
    print(o.get_json())


def test_total_21():
    pass


def test_total_22():
    pass
