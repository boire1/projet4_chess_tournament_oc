class MatchView:
    @classmethod
    def get_result_matches(cls, list_of_matches):
        print("Liste des matchs")
        for m in range(len(list_of_matches)):
            print("Match : ", m + 1)
            print(
                list_of_matches[m].get_player1().get_idp(),
                list_of_matches[m].get_player1().get_firstname(),
                list_of_matches[m].get_player1().get_lastname(),
                "| vs |",
                list_of_matches[m].get_player2().get_idp(),
                list_of_matches[m].get_player2().get_firstname(),
                list_of_matches[m].get_player2().get_lastname(),
            )
            score1 = -1
            score2 = -1
            while True:
                score1 = input(
                    "Entrez un score (1 ou 0 ou 0.5) pour "
                    + str(list_of_matches[m].get_player1().get_firstname())
                    + " : "
                )
                if score1 != "1" and score1 != "0" and score1 != "0.5":
                    print("Le score rentré est invalide !")
                else:
                    score1 = float(score1)
                    break
            if score1 == 1.0:
                score2 = 0.0
            elif score1 == 0.0:
                score2 = 1.0
            else:
                score2 = 0.5
            print("Le score de " + str(list_of_matches[m].get_player2().get_firstname()) + " : " + str(score2))
            if score1 > score2:
                list_of_matches[m].set_winner(1)
            elif score2 > score1:
                list_of_matches[m].set_winner(2)
        print("----------------------------------")
        return list_of_matches

    @classmethod
    def no_registered_match(cls):
        print("Pas de matchs enregistrés")
