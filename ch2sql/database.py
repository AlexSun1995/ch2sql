from ch2sql.tools import similar
from ch2sql.tools.exception import UnknownDataSourceTypeException
from ch2sql.tools.excel import ExcelWrapper


class Table(object):
    def __init__(self, table_name='table', source_type='excel', path=None):
        """
        对不同数据源的表进行包装抽象
        :param table_name: 数据表的名称
        :param source_type: 数据表类型(如'excel', 'mysql' 等)
        :param path: 如果是excel文件,则为本地文件绝对路径否则为数据库URL
        """
        self.table_name = table_name
        self.titles = list()
        self.columns = []
        if source_type == 'excel':
            ex = ExcelWrapper(path)
            for i in range(ex.length):
                title = ex.titles[i]
                assert title is not None
                self.titles.append(title)
                column_type = ex.title_type_dict[title]
                value_list = ex.title_values[title]
                tmp_column = Column(name=ex.titles[i], data_type=column_type, value_list=value_list)
                self.columns.append(tmp_column)
        elif source_type == 'mysql':
            # something to do later..
            pass
        elif source_type == 'sql':
            # something to do later...
            pass
        else:
            raise UnknownDataSourceTypeException("can not handle " + source_type)

    def __iter__(self):
        for column in self.columns:
            yield column

    def get_column_names(self):
        for column in self.columns:
            yield column.name

    def get_column_by_index(self, index):
        """
        获取索引为index的列
        :param index:
        :return: Column
        """
        return self.columns[index]

    def __str__(self):
        print("table name:{}".format(self.table_name))


class Column(object):
    def __init__(self, name='', data_type=None, value_list=None,
                 foreign=False, primary=False, use_relatives=False):
        # 是否在列信息中扩展近义词, 现阶段默认为否
        self.use_relatives = use_relatives
        self._name = name
        self._data_type = data_type
        self.relative_names = self._get_relatives(name)
        self._foreign = foreign
        self._primary = primary
        self._value = value_list

    def _get_relatives(self, name):
        if not self.use_relatives:
            return []
        else:
            return []

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    @property
    def foreign(self):
        return self._foreign

    @property
    def primary(self):
        return self._primary

    def is_relative_word(self, word):
        for _word in self.relative_names:
            if word == _word:
                return True
        return False

    @property
    def relatives(self):
        return self.relative_names

    @property
    def values(self):
        return self._name, self._value

    def values_sample(self, num):
        """
        对column的值集合进行抽样, 抽取出 <= num数量的样本
        :return: []
        """
        values_set = set(self.values[1])
        if len(values_set) <= num:
            return list(values_set)
        else:
            import random
            return random.sample(values_set, num)

    def print_me(self):
        print("test Column.print_me")
