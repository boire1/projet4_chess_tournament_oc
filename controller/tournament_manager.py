from copy import deepcopy

from models.match import Match
from models.round import Round
from views.match_view import MatchView
from views.player_view import PlayerView
from views.top_menu import TopMenu
from views.round_view import RoundView
from views.report_view import ReportView
from views.tournament_view import TournamentView


# ---------------------------------------------------------------------------------
class TournamentManager:
    def __init__(self, db):
        # Choix de l'utilisateur dans le menu
        self.user_choice = 0
        self.db = db
        while self.user_choice != 5:
            self.get_user_choice()
            if self.user_choice == 1:
                TopMenu.create_tournament()
                self.create_tournament()
            elif self.user_choice == 2:
                TopMenu.launch_tournament()
                self.launch_tournament()
            elif self.user_choice == 3:
                TopMenu.create_players()
                self.create_players()
            elif self.user_choice == 4:
                TopMenu.get_tournament_report()
                self.get_tournament_report()
            elif self.user_choice == 5:
                TopMenu.quit()
            else:
                TopMenu.invalid_choice()

    # ---------------------------------------------------------------------------------
    def get_user_choice(self):
        '''Display of the menu'''
        self.user_choice = TopMenu.show_topmenu()

    # ---------------------------------------------------------------------------------
    '''This function create tournaments and also save tournaments'''
    def create_tournament(self):
        # On affiche la liste des joueurs
        players_list = self.db.get_players()
        max_idp = players_list[-1].get_idp()
        PlayerView.show_players_list(players_list)
        # On recupère les informations du nouveau tournoi
        tournament = TournamentView.get_tournament_from_user(max_idp)
        # On enregistre le tournoi
        self.db.save_tournament(tournament)

    # ---------------------------------------------------------------------------------
    ''' This function launch a tournament and display tournament(s) '''
    def launch_tournament(self):
        
        tournaments_list = self.db.get_tournaments()
        max_idt = tournaments_list[-1].get_idt()
        TournamentView.show_tournaments_list(tournaments_list)
        idt = TournamentView.get_tournament_id_from_user(max_idt)
        tournament = self.db.get_tournament(idt)
        rounds = self.db.get_rounds_by_idt(idt)
        """ matches already played"""
        duel_dico = self.get_duel_dico(rounds, tournament.get_players_list_by_ids())
        
        next_round = 1
        round_index = len(rounds) + 1
        if round_index <= tournament.get_number_rounds():
            while next_round == 1 and round_index <= tournament.get_number_rounds():
                RoundView.show_round_index(round_index)
                new_duel_dico, new_matches_ids = self.launch_round(
                    deepcopy(tournament.get_players_list_by_ids()), duel_dico
                )
                duel_dico = new_duel_dico
                round_ = Round()
                round_.set_idt(idt)
                round_.set_number(round_index)
                round_.set_matches_list_by_ids(new_matches_ids)
                self.db.save_round(round_)
                round_index += 1
                if round_index <= tournament.get_number_rounds():
                    while True:
                        next_round = RoundView.to_continue(round_index)
                        if next_round != "1" and next_round != "0":
                            RoundView.invalid_input()
                        else:
                            next_round = int(next_round)
                            break
                else:
                    TournamentView.tournament_ended()
        else:
            TournamentView.tournament_ended()
            
    '''This function create players and also save players'''
    def create_players(self):
        players_list = PlayerView.get_players_from_user()
        self.db.save_players(players_list)
        
    '''This function get list of matches already played'''
    def get_duel_dico(self, rounds, players_list):
        duel_dico = {}
        
        for j in players_list:
            duel_dico[j] = []
        # Recuperation des ids des matchs déjà joués
        if len(rounds) == 0:
            MatchView.no_registered_match()
            return duel_dico
        else:
            # Liste des id match deja joué de ce tournoi
            matches_ids = []
            for r in rounds:
                for idm in r.get_matches_list_by_ids():
                    matches_ids.append(idm)
            old_matches = self.db.get_matches_by_ids(matches_ids)
            # Pour chaque match déjà joué on utilise les données pour mettre à jour duel_dico et score_dico
            # Avant de continuer au tour suivant pour éviter de faire rejouer 2 joueurs qui ont déjà joué
            for m in old_matches:
                duel_dico[m.get_player1().get_idp()].append(m.get_player2().get_idp())
                duel_dico[m.get_player2().get_idp()].append(m.get_player1().get_idp())
            return duel_dico
        
    ''' This function generate matches'''
    def generate_matches(self, players_list_by_ids, duel_dico):
        matches_list = []
        list_tmp = players_list_by_ids
        # Tant qu'on a pas mis tous les joueurs dans un match
        while len(list_tmp) != 0:
            # boolean qui indique est ce qu'un match est initialisé
            set_match = 0
            # Je prend un joueur dans la liste, un par un
            for p1 in list_tmp:
                # Je prend un autre joueur dans la liste, un par un
                for p2 in list_tmp:
                    # Si c'est le meme joueur je passe au joueur suivant
                    if p1 == p2:
                        continue
                    # Je verifie si ils se sont déjà affronté
                    if p2 not in duel_dico[p1]:
                        # Sinon je crée un match
                        match_tmp = Match()
                        match_tmp.set_player1(self.db.get_player(p1))
                        match_tmp.set_player2(self.db.get_player(p2))
                        # J'indique qu'ils se sont affronté dans duel_dico
                        duel_dico[p1].append(p2)
                        duel_dico[p2].append(p1)
                        matches_list.append(match_tmp)
                        # J'indique qu'un match est créé pour pouvoir passer au joueur suivant
                        set_match = 1
                        # Je retire les 2 joueurs dans la liste des joeurs qui ne sont pas encore
                        # dans des matchs pour le tour en cours
                        list_tmp.remove(p1)
                        list_tmp.remove(p2)
                        break
                    # si oui ils se sont affrontés, on vérifie avec le joueur suivant
                # Si un match est créé dans la boucle avec p1, on a pas besoin de continue
                # on reboucle sur la nouvelle liste avec des joueurs non affectés à des matchs
                if set_match == 1:
                    break
        return matches_list, duel_dico
    '''This function operate for rounds'''
    def launch_round(self, players_list_by_ids, duel_dico):
        matches_list, new_duel_dico = self.generate_matches(players_list_by_ids, duel_dico)
        # On demande à l'utilisateur de donner les scores pour le round en cours
        matches_list_upd = MatchView.get_result_matches(matches_list)
        new_matches_ids = self.db.save_matches(matches_list_upd)
        return new_duel_dico, new_matches_ids
    
    ''' This function is for the reporting the individual rankings of players, the total number of wins,losses and drawns, and scores '''    
    def get_tournament_report(self):
               
        """"""
        tournaments_list = self.db.get_tournaments()
        max_idt = tournaments_list[-1].get_idt()
        TournamentView.show_tournaments_list(tournaments_list)
        idt = TournamentView.get_tournament_id_from_user(max_idt)
        tournament = self.db.get_tournament(idt)
        rounds = self.db.get_rounds_by_idt(idt)
        matches_list = self.db.get_matches_by_idt(tournament.get_idt())
        matches_null_list = self.db.get_matches_null_by_idt(tournament.get_idt())
        ReportView.show_tournament_info(tournament, matches_list, matches_null_list)
        players_score = {}
        for idp in tournament.get_players_list_by_ids():
            players_score[idp] = 0
        if len(rounds) == 0:
            ReportView.tournament_not_started()
        else:
            for round in rounds:
                matches_list = self.db.get_matches_by_ids(round.get_matches_list_by_ids())
                matches_null_list = self.db.get_matches_null_by_ids(round.get_matches_list_by_ids())
                ReportView.show_round_report(round, matches_list, matches_null_list, players_score)
        ReportView.show_top_list_title()
        players_sorted = sorted(players_score, key=lambda x: players_score[x], reverse=True)
        for i in range(len(players_sorted)):
            player = self.db.get_player(players_sorted[i])
            ReportView.show_player_info(i, players_score, players_sorted, player)
