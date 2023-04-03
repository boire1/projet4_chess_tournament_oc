from models.player import Player


class Match:
    def __init__(self, idm=-1, player1=Player(), player2=Player(), winner=0):
        self.idm = idm
        self.player1 = player1
        self.player2 = player2
        self.winner = winner

    def to_dict(self):
        return {
            "idm": self.idm,
            "player1": self.player1.get_idp(),
            "player2": self.player2.get_idp(),
            "winner": self.winner,
        }

    def get_idm(self):
        return self.idm

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_winner(self):
        return self.winner

    def set_idm(self, idm):
        self.idm = idm

    def set_player1(self, player1):
        self.player1 = player1

    def set_player2(self, player2):
        self.player2 = player2

    def set_winner(self, winner):
        self.winner = winner
