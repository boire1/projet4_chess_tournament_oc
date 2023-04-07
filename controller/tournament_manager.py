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
    def create_tournament(self):
        '''This function create tournaments and also save tournaments'''
        
        players_list = self.db.get_players()
        max_idp = players_list[-1].get_idp()
        PlayerView.show_players_list(players_list)
        
        tournament = TournamentView.get_tournament_from_user(max_idp)
        
        self.db.save_tournament(tournament)

    # ---------------------------------------------------------------------------------
    
    def launch_tournament(self):
        ''' This function launch a tournament and display tournament(s) '''
        
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
            
    
    def create_players(self):
        '''This function create players and also save players'''
        players_list = PlayerView.get_players_from_user()
        self.db.save_players(players_list)
        
    
    def get_duel_dico(self, rounds, players_list):
        '''This function get list of matches already played'''
        
        duel_dico = {}
        
        for j in players_list:
            duel_dico[j] = []
        
        if len(rounds) == 0:
            MatchView.no_registered_match()
            return duel_dico
        else:
            
            matches_ids = []
            for r in rounds:
                for idm in r.get_matches_list_by_ids():
                    matches_ids.append(idm)
            old_matches = self.db.get_matches_by_ids(matches_ids)
            
            for m in old_matches:
                duel_dico[m.get_player1().get_idp()].append(m.get_player2().get_idp())
                duel_dico[m.get_player2().get_idp()].append(m.get_player1().get_idp())
            return duel_dico
        
    
    def generate_matches(self, players_list_by_ids, duel_dico):
        ''' This function generate matches'''
        matches_list = []
        list_tmp = players_list_by_ids
        
        while len(list_tmp) != 0:
            
            set_match = 0
            
            for p1 in list_tmp:
                
                for p2 in list_tmp:
                    
                    if p1 == p2:
                        continue
                    
                    if p2 not in duel_dico[p1]:
                        
                        match_tmp = Match()
                        match_tmp.set_player1(self.db.get_player(p1))
                        match_tmp.set_player2(self.db.get_player(p2))
                        
                        duel_dico[p1].append(p2)
                        duel_dico[p2].append(p1)
                        matches_list.append(match_tmp)
                        
                        set_match = 1
                        
                        list_tmp.remove(p1)
                        list_tmp.remove(p2)
                        break
                    
                
                
                if set_match == 1:
                    break
        return matches_list, duel_dico
    
    def launch_round(self, players_list_by_ids, duel_dico):
        
        matches_list, new_duel_dico = self.generate_matches(players_list_by_ids, duel_dico)
        
        matches_list_upd = MatchView.get_result_matches(matches_list)
        new_matches_ids = self.db.save_matches(matches_list_upd)
        return new_duel_dico, new_matches_ids
    
       
    def get_tournament_report(self):
        ''' This function is for the reporting the individual rankings of players, the total number of wins,losses and drawns, and scores ''' 
               
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
