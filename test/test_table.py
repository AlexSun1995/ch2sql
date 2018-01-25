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
    print(excel.title_type_dict['日期'])  # why is text? maybe it's the xlrd module's problem
    # todo
    assert excel.title_type_dict['日期'] == 'date'


def test_table():
    print("test excel 01")
    from ch2sql.database import Table
    import os
    path = "../datasource/广告投放效果2.xls"
    assert os.path.exists(path)
    path = os.path.abspath(path)
    print(path)
    table = Table(table_name='广告投放效果',path=path)
    # print(list(table.column_names()))
    assert len((list(table.column_names()))) > 0
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
    assert table.columns