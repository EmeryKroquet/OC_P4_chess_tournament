class Player:

    def __init__(
        self, first_name: str,
            last_name: str,
            date_of_birth: str,
            gender: str,
            rating: int,
            id_number: int,
            delete_player: bool
    ):
        """Constructeur pour le joueur.
        Arguments :
            first_name (str) : Le prénom du joueur.
            Last_name (str) : Le nom de famille du joueur.
            Date_of_birth (str) : Date de naissance du joueur.
            Gender (str) : Sexe du joueur.
            rating (int) : Classement ELO du joueur.
            Id_number (int) : Numéro d'identification unique du joueur.
            Delete_player (bool) : Le joueur est-il supprimé ?
        """

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.rating = rating
        self.id_number = id_number
        self.delete_player = delete_player

    def __str__(self):
        show_info = " - Player ID: {id}\n".format(id=self.id_number) +\
                    "   - First Name: {first_name}\n".format(first_name=self.first_name)
        show_info += "   - Last Name: {last_name}\n".format(last_name=self.last_name)
        show_info += "   - Date of birth: {dob}\n".format(dob=self.date_of_birth)
        show_info += "   - Gender: {gender}\n".format(gender=self.gender)
        show_info += "   - Rating: {rating}\n".format(rating=str(self.rating))
        show_info += "   - Is deleted: {deleted}\n".format(deleted=str(self.delete_player))

        return show_info
