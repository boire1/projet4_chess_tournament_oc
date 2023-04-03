class Tournament:
    def __init__(
        self,
        idt=-1,
        name="",
        place="",
        date="",
        number_rounds=0,
        players_list=[],
        players_list_by_ids=[],
    ):
        self.idt = idt
        self.name = name
        self.place = place
        self.date = date
        self.number_rounds = number_rounds
        self.players_list = players_list
        self.players_list_by_ids = players_list_by_ids

    def to_dict(self):
        return {
            "idt": self.idt,
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "number_rounds": self.number_rounds,
            "players_list_by_ids": self.get_players_list_by_ids(),
        }

    def get_idt(self):
        return self.idt

    def get_name(self):
        return self.name

    def get_place(self):
        return self.place

    def get_date(self):
        return self.date

    def get_number_rounds(self):
        return self.number_rounds

    def get_players_list(self):
        return self.players_list

    def get_players_list_by_ids(self):
        if len(self.players_list) > 0:  # ???
            for player in self.players_list:
                self.players_list_by_ids.append(player.get_idp())
            return self.players_list_by_ids
        else:
            return self.players_list_by_ids

    def set_idt(self, idt):
        self.idt = idt

    def set_name(self, name):
        self.name = name

    def set_place(self, place):
        self.place = place

    def set_date(self, date):
        self.date = date

    def set_number_rounds(self, number_rounds):
        self.number_rounds = number_rounds

    def set_players_list(self, players_list):
        self.players_list = players_list

    def set_players_list_by_ids(self, players_list_by_ids):
        self.players_list_by_ids = players_list_by_ids
