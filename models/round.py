class Round:
    def __init__(self, idt=-1, number=-1, matches_list=[], matches_list_by_ids=[]):
        self.idt = idt
        self.number = number
        self.matches_list = matches_list
        self.matches_list_by_ids = matches_list_by_ids

    def to_dict(self):
        return {
            "idt": self.idt,
            "number": self.number,
            "matches_list_by_ids": self.get_matches_list_by_ids(),
        }

    def get_idt(self):
        return self.idt

    def get_number(self):
        return self.number

    def get_matches_list_by_ids(self):
        if len(self.matches_list) > 0:
            for match in self.matches_list:
                self.matches_list_by_ids.append(match.get_idm())
            return self.matches_list_by_ids
        else:
            return self.matches_list_by_ids

    def set_idt(self, idt):
        self.idt = idt

    def set_number(self, number):
        self.number = number

    def set_matches_list_by_ids(self, matches_list_by_ids):
        self.matches_list_by_ids = matches_list_by_ids
