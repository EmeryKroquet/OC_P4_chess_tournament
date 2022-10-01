class Player:

    def __init__(self, first_name: str, last_name: str,
                 date_of_birth: str, rating: int,
                 gender: str, id_number: int,
                 delete_player: bool
                 ):
        self.rating = rating
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.id_number = id_number
        self.delete_player = delete_player

    def __str__(self):
        stdout_content = " - Player ID: {id}\n".format(id=self.id_number)
        stdout_content += "   - First Name: {first_name}\n".format(first_name=self.first_name)
        stdout_content += "   - Last Name: {last_name}\n".format(last_name=self.last_name)
        stdout_content += "   - DOB: {dob}\n".format(dob=self.date_of_birth)
        stdout_content += "   - Gender: {gender}\n".format(gender=self.gender)
        stdout_content += "   - Rating: {elo}\n".format(elo=str(self.rating))
        stdout_content += "   - Player deleted: {deleted}\n".format(deleted=str(self.delete_player))

        return stdout_content
