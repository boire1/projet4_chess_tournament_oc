class RoundView:
    @classmethod
    def show_round_index(cls, round_index):
        print("Round Index : ", round_index)

    @classmethod
    def to_continue(cls, round_index):
        return input("Continuer au prochain au round " + str(round_index) + "? Entrez 1 si OUI, 0 si NON : ")

    @classmethod
    def invalid_input(cls):
        print("Veuillez repondre pas 1 si OUI, 0 si NON !")
