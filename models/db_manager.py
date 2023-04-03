import json
from models.tournament import Tournament
from models.match import Match
from models.player import Player
from models.round import Round


# ------------------------------- -----------------------------------------------------------------------
class DBManager:
    def __init__(self):
        pass

    def get_players(self):
        players_list = []
        players_dico = None
        with open("./database/players.json", "r") as file:
            players_dico = json.load(file)
        for player in players_dico:
            p = Player()
            p.set_idp(player["idp"])
            p.set_firstname(player["firstname"])
            p.set_lastname(player["lastname"])
            p.set_birthdate(player["birthdate"])
            p.set_gender(player["gender"])
            players_list.append(p)
        return players_list

    def get_tournaments(self):
        tournaments_list = []
        tournaments_dico = None
        with open("./database/tournament.json", "r") as file:
            tournaments_dico = json.load(file)
        for tournament in tournaments_dico:
            t = Tournament()
            t.set_idt(tournament["idt"])
            t.set_name(tournament["name"])
            t.set_place(tournament["place"])
            t.set_date(tournament["date"])
            t.set_number_rounds(tournament["number_rounds"])
            t.set_players_list_by_ids(tournament["players_list_by_ids"])
            tournaments_list.append(t)
        return tournaments_list

    def get_tournament(self, idt):
        tournaments_list = self.get_tournaments()
        for t in tournaments_list:
            if t.get_idt() == idt:
                return t

    def get_player(self, idp):
        players_list = self.get_players()
        for p in players_list:
            if p.get_idp() == idp:  # ??
                return p

    def get_rounds(self):
        rounds_list = []
        rounds_dico = None
        with open("./database/round.json") as file:
            rounds_dico = json.load(file)
        for round in rounds_dico:
            r = Round()
            r.set_idt(round["idt"])
            r.set_number(round["number"])
            r.set_matches_list_by_ids(round["matches_list_by_ids"])
            rounds_list.append(r)
        return rounds_list

    def get_rounds_by_idt(self, idt):
        rounds_list = self.get_rounds()
        ret_rounds_list = []  # ??
        for r in rounds_list:
            if r.get_idt() == idt:
                ret_rounds_list.append(r)
        return ret_rounds_list

    def get_matches(self):
        matches_list = []
        matches_dico = None
        with open("./database/match.json") as file:
            matches_dico = json.load(file)
        for match in matches_dico:
            m = Match()
            m.set_idm(match["idm"])
            m.set_player1(self.get_player(match["player1"]))
            m.set_player2(self.get_player(match["player2"]))
            m.set_winner(match["winner"])
            matches_list.append(m)
        return matches_list

    def get_matches_by_ids(self, ids_list):  # ids
        matches_list = self.get_matches()
        ret_matches_list = []
        for m in matches_list:
            if m.get_idm() in ids_list:
                ret_matches_list.append(m)
        return ret_matches_list

    def get_matches_null_by_ids(self, ids_list):
        matches_list = self.get_matches()
        ret_matches_list = []
        for m in matches_list:
            if m.get_idm() in ids_list and m.get_winner() == 0:
                ret_matches_list.append(m)
        return ret_matches_list

    def get_matches_by_idt(self, idt):
        matches_ids_list = []
        rounds = self.get_rounds_by_idt(idt)
        for round in rounds:
            matches_ids_list = matches_ids_list + round.get_matches_list_by_ids()
        return self.get_matches_by_ids(matches_ids_list)

    def get_matches_null_by_idt(self, idt):
        matches_ids_list = []
        rounds = self.get_rounds_by_idt(idt)
        for round in rounds:
            matches_ids_list = matches_ids_list + round.get_matches_list_by_ids()
        return self.get_matches_null_by_ids(matches_ids_list)

    # ------------------------------- -----------------------------------------------------------------------

    def save_tournament(self, tournament):
        tournament.set_idt(self.get_new_tournament_id())
        with open("./database/tournament.json", "r") as file:
            old_tournaments = json.load(file)
            new_tournaments = old_tournaments + [tournament.to_dict()]
            with open("./database/tournament.json", "w") as file:
                json.dump(new_tournaments, file, indent=2)

    def save_round(self, round_):
        with open("./database/round.json", "r") as file:
            old_rounds = json.load(file)
            new_rounds = old_rounds + [round_.to_dict()]
            with open("./database/round.json", "w") as file:
                json.dump(new_rounds, file, indent=2)

    def save_players(self, players_list):  # idp index player
        idp = self.get_new_player_id() - 1
        new_players = []
        for p in players_list:
            idp += 1
            p.set_idp(idp)
            new_players.append(p.to_dict())
        with open("./database/players.json", "r") as file:
            old_players = json.load(file)
            news_players_dict = old_players + new_players
            with open("./database/players.json", "w") as file:
                json.dump(news_players_dict, file, indent=2)

    def save_matches(self, matches_list):
        idm = self.get_new_match_id() - 1
        new_matches = []
        new_matches_ids = []
        for m in matches_list:
            idm += 1
            m.set_idm(idm)
            new_matches_ids.append(idm)
            new_matches.append(m.to_dict())
        with open("./database/match.json", "r") as file:
            old_matches = json.load(file)
            new_matches_dict = old_matches + new_matches
            with open("./database/match.json", "w") as file:
                json.dump(new_matches_dict, file, indent=2)
        return new_matches_ids

    # ------------------------------- -----------------------------------------------------------------------

    def get_new_tournament_id(self):
        tournaments = None
        with open("./database/tournament.json", "r") as file:
            tournaments = json.load(file)
        return len(tournaments)

    def get_new_player_id(self):
        players = None
        with open("./database/players.json", "r") as file:
            players = json.load(file)
        return len(players)

    def get_new_match_id(self):
        matches = None
        with open("./database/match.json", "r") as file:
            matches = json.load(file)
        return len(matches)
