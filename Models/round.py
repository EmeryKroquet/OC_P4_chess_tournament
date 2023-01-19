class Round:

    def __init__(self, number_of_round: int, tournament_id: int, id_number: int):
        """Constructeur pour le rond.

        Arguments :
            number_of_round (int) : Numéro de ronde ordonné dans le tournoi.
            Tournament_id (int) : Identifiant unique du tournoi parent.
            id_number (int) : Identifiant unique de ce tour.
        """

        self.number_of_round = number_of_round
        self.tournament_id = tournament_id
        self.id_number = id_number

        self.matches = {}

    def __str__(self):
        show_info = "   - Number of tours: {num}\n".format(num=self.number_of_round) + "   - Matches -\n"

        for started_match in self.matches:
            show_info += started_match.__str__()

        return show_info
