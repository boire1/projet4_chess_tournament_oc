class ReportView:
    @classmethod
    def show_tournament_info(cls, tournament, matches_list, matches_null_list):
        print("=======================================================================")
        print("TOURNOI -", tournament.get_name())
        print("\t Lieu", tournament.get_place())
        print("\t Date", tournament.get_date())
        print("\t Nombre de machs totals", len(matches_list))
        print("\t Nombre de machs nuls", len(matches_null_list))

    @classmethod
    def tournament_not_started(cls):
        print("Ce tournoi n'a pas encore commencé !")

    @classmethod
    def show_round_report(cls, round, matches_list, matches_null_list, players_score):
        print("-------------------- Round " + str(round.get_number()) + "--------------------")
        print("\t Nombre de matchs :", len(matches_list))
        print("\t Nombre de matchs nuls :", len(matches_null_list))
        print("\t Matches :")
        for m in matches_list:
            score_p1 = 0
            score_p2 = 0
            if m.get_winner() == 1:
                score_p1 = 1
            elif m.get_winner() == 2:
                score_p2 = 1
            else:
                score_p1 = 0.5
                score_p2 = 0.5
            players_score[m.get_player1().get_idp()] += score_p1
            players_score[m.get_player2().get_idp()] += score_p2
            print(
                "\t \t"
                + "("
                + str(m.get_player1().get_idp())
                + ") "
                + (str(m.get_player1().get_firstname()) + " " + str(m.get_player1().get_lastname()))[:10]
                + "\t\t"
                + str(score_p1)
                + "\t"
                + str(score_p2)
                + "\t\t"
                + "("
                + str(m.get_player2().get_idp())
                + ")"
                + " "
                + (str(m.get_player2().get_firstname()) + " " + str(m.get_player2().get_lastname()))[:10]
            )

    @classmethod
    def show_top_list_title(cls):
        print("-------------------- Classement des joueurs --------------------")

    @classmethod
    def show_player_info(cls, i, players_score, players_sorted, player):
        print(
            i + 1,
            "(" + str(player.get_idp()) + ")",
            (str(player.get_firstname()) + " " + str(player.get_lastname()))[:10],
            ":",
            players_score[players_sorted[i]],
        )
