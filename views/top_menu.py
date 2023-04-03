class TopMenu:
    @classmethod
    def show_topmenu(cls):
        print()
        user_choice = 0
        print()
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("'", "\t", "Menu général", "    '")
        print("'", "\t", "du Tournoi d'échec", "'")
        print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        print("(1) Créer un tournoi")
        print("(2) Lancer un tournoi")
        print("(3) Créer des joueurs")
        print("(4) Voir les rapports d'un tournoi")
        print("(5) Quit")
        print("_-_-_-_-_-_-_-_-_-_-_-_-_-: ")
        while True:
            user_choice = input("choose --> : ")
            if not user_choice.isdigit():
                print("Le choix est invalide !")
            elif user_choice not in ["1", "2", "3", "4", "5"]:
                print("Le choix est invalide !")
            else:
                break
        return int(user_choice)

    @classmethod
    def create_tournament(cls):
        print("\nCréation d'un tournoi\n")

    @classmethod
    def launch_tournament(cls):
        print("\nLancement d'un tournoi\n")

    @classmethod
    def create_players(cls):
        print("\nCréation de joueurs\n")

    @classmethod
    def get_tournament_report(cls):
        print("\nRapport d'un tournoi\n")

    @classmethod
    def quit(cls):
        print("-----------(( -> ))----------------")
        print("Vous avez quittez avec succès !")
        print("-----------(( -> ))----------------")

    @classmethod
    def invalid_choice(cls):
        print("Choix invalide !")
