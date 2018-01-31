import xlrd


class ExcelWrapper(object):
    def __init__(self, data_source, value_size_limit=1000):
        # 在数据表取列值的数量限制,防止表过大
        self.value_size_limit = value_size_limit
        self.data_source = data_source
        self.work_book = xlrd.open_workbook(data_source)
        # type: list
        self.titles,self.length = self._get_titles()
        # type: dict
        self.title_values = self._get_values()
        # type: dict
        self.title_type_dict = self._get_title_types()

    def _get_titles(self):
        self.sheet = self.work_book.sheet_by_index(0)
        sheet = self.sheet
        assert sheet is not None
        _titles = sheet.row_values(0)
        tmp = []
        for title in _titles:
            tmp.append(title)
        assert len(tmp) > 0
        return tmp, len(tmp)

    def _get_values(self):
        """
        :return: key-value pair, where key is column name, value
        is a value list of column
        """
        tmp = {}
        for i in range(self.length):
            column_name = self.titles[i]
            if column_name not in tmp.keys():
                tmp[column_name] = []
            cols = self.sheet.col_values(i)
            assert len(cols) > 1
            for j in range(1, len(cols)):
                tmp[column_name].append(cols[j])
        return tmp

    def _get_title_types(self):
        tmp = {}
        for i in range(self.length):
            title = self.titles[i]
            # just the cell below the title
            _type_id = self.sheet.cell_type(1, i)
            if _type_id == 0:
                type_name = 'empty'
            elif _type_id == 1:
                type_name = 'text'
            elif _type_id == 2:
                type_name = 'number'
            elif _type_id == 3:
                type_name = 'date'
            elif _type_id == 4:
                type_name = 'bool'
            else:
                type_name = 'unknown'
            tmp[title] = type_name
        return tmp
