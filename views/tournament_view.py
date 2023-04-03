from datetime import date

from models.tournament import Tournament


class TournamentView:
    @classmethod
    def get_tournament_from_user(cls, max_idp):
        print("----------------------------------")
        print("Info du tournoi")
        tournament = Tournament()
        while True:
            tournament.set_name(input("Entrez le nom du tournoi svp >> "))
            n_name = tournament.get_name()
            n_name = n_name.lstrip()
            n_name = n_name.capitalize()
            tournament.set_name(n_name)
            if len(tournament.get_name()) < 3:
                print("Le nom est trop court !")
            elif len(tournament.get_name()) > 20:
                print("Le nom est trop long !")
            elif any(map(lambda x: x.isdigit(), tournament.get_name())):
                print("Le nom ne doit pas contenir de chiffres !")
            else:
                break
        while True:
            tournament.set_place(input("Entrez place --> : "))
            n_place = tournament.get_place()
            n_place = n_place.lstrip()
            n_place = n_place.capitalize()
            tournament.set_place(n_place)
            if len(tournament.get_place()) < 3:
                print("Le nom du lieu trop court !")
            elif len(tournament.get_place()) > 20:
                print("Le nom du lieu est trop long !")
            elif any(map(lambda x: x.isdigit(), tournament.get_place())):
                print("Le nom du lieu ne doit pas contenir de chiffres !")
            else:
                break
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")
        tournament.set_date(date_string)
        tournament.set_number_rounds(4)
        players_list_by_ids = []
        for i in range(8):
            idp = -1
            while True:
                idp = input("Entrez l'id du joueur " + str(i + 1) + "/8 : ")
                if not idp.isdigit():
                    print("L'id doit etre un nombre !")
                elif int(idp) > max_idp and int(idp) >= 0:
                    print("Ce joueur n'est pas dans la liste !")
                elif int(idp) in players_list_by_ids:
                    print("Ce joueur est déjà choisi !")
                else:
                    break
            players_list_by_ids.append(int(idp))
        tournament.set_players_list_by_ids(players_list_by_ids)
        return tournament

    @classmethod
    def get_tournament_id_from_user(cls, max_idt):
        # On demande à l'utilisateur de choisir un tournoi
        idt = -1
        while True:
            idt = input("Entrez l'id du tournoi --> : ")
            if not idt.isdigit():
                print("L'id doit etre un nombre ")
            elif int(idt) > max_idt and int(idt) >= 0:
                print("Ce tournoi choisi n'est pas dans la liste !")
            else:
                break
        return int(idt)

    @classmethod
    def show_tournaments_list(cls, tournaments_list):
        print("======================= Liste des Tournois =================================")
        for t in tournaments_list:
            print(t.get_idt(), t.get_name(), t.get_place(), t.get_date())

    @classmethod
    def tournament_ended(cls):
        print("Tournoi terminé !")
