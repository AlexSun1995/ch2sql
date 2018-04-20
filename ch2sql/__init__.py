# 识别数据库，从数据库中提取出元信息
# 用jieba, LTP对查询语句进行处理
# 识别查询目标，找出select 后面的内容
# 对提取目标相关的条件约束，重点对ATT关系进行处理 相当于进行where填充

from ch2sql.database import Column


def _get_target(sentence):
    """
    :param type(sentence): Sentence
    :return: str: the target sentence of this search
    eg. "销售量大于100万的销售员" -> "销售员"
    """
    pass


if __name__ == '__main__':
    test = Column()
    print(test.print_me())
