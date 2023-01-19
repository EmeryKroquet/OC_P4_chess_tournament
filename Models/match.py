class Match:

    def __init__(self, players: tuple, tournament_id: int, round_id: int, player_winner: int, id_number: int):
        """Constructeur pour Match.

               Arguments :
                   joueurs (tuple [Player]) : Les deux joueurs participants.
                   tournament_id (int) : Identifiant unique du tournoi parent.
                   round_id (int) : Identifiant unique du tour parent.
                   Player_winner (int) : Gagnant du match. 1 pour le joueur 1, 2
                    pour le joueur 2, 0 pour un match nul et Aucun si TBD.
                   Id_number (int) : Identifiant unique de ce match.
               """

        self.tournament_id = tournament_id
        self.round_id = round_id
        self.winner = player_winner
        self.id_number = id_number

        self.player_1 = players[0]
        self.player_2 = players[1]

    def __str__(self):
        show_info = "    - {first_name_1} {last_name_1} ({rating_1}) vs {first_name_2}" \
                    " {last_name_2} ({rating_2})\n".format(first_name_1=self.player_1.first_name,
                                                           last_name_1=self.player_1.last_name,
                                                           rating_1=self.player_1.rating,
                                                           first_name_2=self.player_2.first_name,
                                                           last_name_2=self.player_2.last_name,
                                                           rating_2=self.player_2.rating,
                                                           )
        show_info += "    Winner : {winner}\n".format(winner=self.winner)
        show_info += "    id : {id}\n".format(id=self.id_number)

        return show_info
