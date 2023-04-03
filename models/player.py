class Player:
    def __init__(self, idp=-1, firstname="", lastname="", birthdate="", gender=""):
        self.idp = idp
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.gender = gender

    def to_dict(self):
        return {
            "idp": self.idp,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
        }

    def get_idp(self):
        return self.idp

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_birthdate(self):
        return self.birthdate

    def get_gender(self):
        return self.gender

    def set_idp(self, idp):
        self.idp = idp

    def set_firstname(self, firstname):
        self.firstname = firstname

    def set_lastname(self, lastname):
        self.lastname = lastname

    def set_birthdate(self, birthdate):
        self.birthdate = birthdate

    def set_gender(self, gender):
        self.gender = gender
