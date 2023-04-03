from controller.tournament_manager import TournamentManager
from models.db_manager import DBManager


def main():
    db = DBManager()
    TournamentManager(db)


if __name__ == "__main__":
    main()
