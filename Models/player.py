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
        show_info = f" - Player ID: {self.id_number}\n"
        show_info += f" - First Name: {self.first_name}\n"
        show_info += f" - Last Name: {self.last_name}\n"
        show_info += f" - Date Of Birth: {self.date_of_birth}\n"
        show_info += f" - Gender: {self.gender}\n"
        show_info += f" - Rating: {str(self.rating)}\n"
        show_info += f" - Player Delete: {str(self.delete_player)}"

        return show_info
