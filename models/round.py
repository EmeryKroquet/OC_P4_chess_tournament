class Round:

    def __init__(self, round_number: int, tournament_id: int, id_number: int):

        self.round_number = round_number
        self.tournament_id = tournament_id
        self.id_number = id_number

        self.matches = {}

    def __str__(self):
        stdout_content = "   - Round Number: {num}\n".format(num=self.round_number)

        stdout_content += "   - Matches -\n"

        for started_match in self.matches:
            stdout_content += started_match.__str__()

        return stdout_content
