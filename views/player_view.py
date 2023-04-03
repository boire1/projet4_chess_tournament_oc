from models.player import Player
from datetime import datetime


class PlayerView:
    @classmethod
    def get_players_from_user(cls):
        players_list = []
        create_new_player = True
        while create_new_player:
            print("|================================================|")
            print("\t", "Création de joueur")
            print("|================================================|")
            player = Player()
            while True:
                player.set_firstname(input("Entrez un prenom de joueur svp >> "))
                n_firstname = player.get_firstname()
                n_firstname = n_firstname.lstrip()
                n_firstname = n_firstname.capitalize()
                player.set_firstname(n_firstname)
                if len(player.get_firstname()) < 3:
                    print("Le prénom est trop court !")
                elif len(player.get_firstname()) > 20:
                    print("Le prénom est trop long !")
                elif any(map(lambda x: x.isdigit(), player.get_firstname())):
                    print("Le prénom ne doit pas contenir de chiffres !")
                else:
                    break
            while True:
                player.set_lastname(input("Entrez un nom de joueur svp >> "))
                n_lastname = player.get_lastname()
                n_lastname = n_lastname.lstrip()
                n_lastname = n_lastname.capitalize()
                player.set_lastname(n_lastname)
                if len(player.get_lastname()) < 3:
                    print("Le nom est trop court !")
                elif len(player.get_lastname()) > 20:
                    print("Le nom est trop long !")
                elif any(map(lambda x: x.isdigit(), player.get_lastname())):
                    print("Le nom ne doit pas contenir de chiffres !")
                else:
                    break
            while True:
                try:
                    date_string = input("Entrez une date de naissance pour le joueur au format YYYY-MM-DD : ")
                    date = datetime.strptime(date_string, "%Y-%m-%d")
                    break
                except ValueError:
                    print("La date saisie est invalide, veuillez réessayer.")
            formatted_date = date.strftime("%Y-%m-%d")
            player.set_birthdate(formatted_date)
            while True:
                player.set_gender(input("Entrez le genre du joueur (h ou f) >> "))
                if player.get_gender() != "h" and player.get_gender() != "f":
                    print("Le genre n'est pas valide !")
                else:
                    break
            players_list.append(player)
            create_new_player = input("Saisir un nouveau joueur ? (y/n)") == "y"
        return players_list

    @classmethod
    def show_players_list(cls, players_list):
        print("======================= Liste des Joueurs =================================")
        for p in players_list:
            print(p.get_idp(), p.get_firstname(), p.get_lastname(), p.get_gender())
