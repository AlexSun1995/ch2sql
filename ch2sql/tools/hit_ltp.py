import jieba
import os


class LtpParser(object):
    """
    哈工大LTP工具的使用包装. git clone以后这里的代码需要修改,
    要将ltp_path 的路径改为本地机器存储ltp模型文件的路径. 模型文件
    较大, 无法随项目一起上传
    """
    default_ltp_api_key = "s1n5k7M9i5zXTqamAy3V1U7CkwskygraFX5fpKyH"
    # 路径变化这里需要修改
    ltp_path = "/Users/alexsun/codes/nlp/ltp_practice/ltp_model/ltp_data"
    @staticmethod
    def cutting(sentence, table=None):
        """
        :param sentence: 输入的查询语句
        :param table: 数据表格对应的Table
        :return: 分词结果
        """
        # 根据数据库字段信息更新jieba分词词典,确保表的关键词不能分开
        if table is None:
            return list(jieba.cut(sentence))
        suggest_words = list(table.get_column_names())
        for column in table:
            if column.data_type != "text":
                continue
            tmp = column.values_sample(100)
            for v in tmp:
                suggest_words.append(v)
        for word in suggest_words:
            if word != " " and word is not None and type(word) == str:
                jieba.suggest_freq(word, True)
        ans = list(jieba.cut(sentence, HMM=True))
        return ans

    @staticmethod
    def pos_tagging(cutting_list):
        pos_model_path = os.path.join(LtpParser.ltp_path, 'pos.model')
        from pyltp import Postagger
        pos_tagger = Postagger()
        pos_tagger.load(pos_model_path)
        tags = pos_tagger.postag(cutting_list)
        pos_tagger.release()
        return tags

    @staticmethod
    def entity_recognize(cutting_list, tagging_list):
        ner_model_path = os.path.join(LtpParser.ltp_path, 'ner.model')
        from pyltp import NamedEntityRecognizer
        recognizer = NamedEntityRecognizer()
        recognizer.load(ner_model_path)
        ne_tags = recognizer.recognize(cutting_list, tagging_list)
        recognizer.release()
        return ne_tags

    @staticmethod
    def dependency_parsing(cutting_list, tagging_list):
        """
        依存句法分析
        :param cutting_list: 分词列表
        :param tagging_list: 词性标注列表
        :return:依存分析的结果
        """
        # 依存句法分析
        par_model_path = os.path.join(LtpParser.ltp_path, 'parser.model')
        from pyltp import Parser
        parser = Parser()
        parser.load(par_model_path)
        arcs = parser.parse(cutting_list, tagging_list)
        parser.release()
        return arcs


    @staticmethod
    def getting_by_cloud(sentence, api_key=default_ltp_api_key, pattern='dp'):
        """
        调用语言云进行分词、词性标注、命名实体识别。
        http://api.ltp-cloud.com/
       （测试阶段使用，调用语言云就不能更新分词词典）
        :param sentence:
        :param api_key:
        :param pattern: ws: 分词, pos:词性标注, ner: 命名实体识别
        dp:依存语法分析, srl:语义角色标注
        :return:
        """
        import urllib.request
        url_get_base = u"http://api.ltp-cloud.com/analysis/?"
        args = {
            'api_key': api_key,
            'text': sentence,
            'pattern': pattern,
            'format': 'plain'
        }
        url = url_get_base + urllib.parse.urlencode(args)
        # print(url)
        result = urllib.request.urlopen(url)
        content = result.read().strip()
        return content.decode('utf-8')

    @staticmethod
    def getting_all_by_cloud(sentence):
        patterns = ['ws', 'pos', 'ner', 'dp', 'srl']
        for pattern in patterns:
            result = LtpParser.getting_by_cloud(sentence, pattern=pattern)
            print('pattern type:{}'.format(pattern))
            print(result)
