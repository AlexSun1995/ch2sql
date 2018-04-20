"""
    -----json type-------
    select:
    condition_and:
    condition_or:
    order_by_desc:
    order_by_asc:
    group_by:
    having:
    result_limit:
    from_date:
    to_date:
    ---------------------

"""
import json


class Output(object):
    def __init__(self, parser):
        self.parser = parser
        self.dict = dict()
        self.extract_information()

    def extract_information(self):
        targets = self.parser.select_targets
        self.dict["select"] = []
        for t in targets:
            self.dict["select"].append(str(t))
        self.dict["condition_and"] = []
        self.dict["condition_or"] = []
        conditions = self.parser.conditions
        for i in range(len(conditions)):
            if i == 0:
                self.dict["condition_and"].append(conditions[0].to_string())
            else:
                if conditions[i - 1].relation_with_next == 'AND':
                    self.dict["condition_and"].append(conditions[i].to_string())
                elif conditions[i - 1].relation_with_next == 'OR':
                    self.dict["condition_or"].append(conditions[i].to_string())

        self.dict["order_by_desc"] = []
        self.dict["group_by"] = []
        self.dict["having"] = []
        self.dict["result_limit"] = None
        self.dict["date_from"] = None
        self.dict["date_to"] = None
        # tackle with top nodes
        tops = self.parser.top_attribute_and_number
        for t in tops:
            if len(self.dict["select"]) == 0 or self.dict["select"][0] != 'ALL':
                try:
                    self.dict["select"].index(t[0])
                    pass
                except ValueError:
                    self.dict["select"].append(t[0])
            self.dict["order_by_desc"].append(t[0])
            if self.dict["result_limit"] is None:
                self.dict["result_limit"] = t[1]
            else:
                self.dict["result_limit"] = min(t[1], self.dict["result_limit"])

        groups = self.parser.group_by_attribute
        for g in groups:
            if len(self.dict["select"]) == 0 or self.dict["select"][0] != 'ALL':
                try:
                    self.dict["select"].index(g)
                    pass
                except ValueError:
                    self.dict["select"].append(g)
            self.dict["group_by"].append(g)

        self.dict["date_from"] = str(self.parser.date_from)
        self.dict["date_to"] = str(self.parser.date_to)

    def get_json(self):
        return json.dumps(self.dict, ensure_ascii=False, indent=4)

