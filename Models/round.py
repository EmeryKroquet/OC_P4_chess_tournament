class Round:

    def __init__(self, round_number: int, tournament_id: int, id_number: int):
        self.round_number = round_number
        self.tournament_id = tournament_id
        self.id_number = id_number

        self.matches = {}

    def __str__(self):
        show_info = (f"   - Round Number: {self.round_number}\n"

                     f"   - Matches -\n")

        for started_match in self.matches:
            show_info += started_match.__str__()

        return show_info
