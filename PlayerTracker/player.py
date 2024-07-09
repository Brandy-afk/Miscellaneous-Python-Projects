import datetime

# Class intended for packaging player data.
class Player():
    def __init__(self, first_name: str, last_name: str, sport: str, team: str,
                 number: int, position: str, points: int, fouls: int):
        self.first_name = first_name
        self.last_name = last_name
        self.sport = sport
        self.team = team
        self.number = number
        self.position = position
        self.date_added = datetime.datetime.now().strftime("%d/%m/%Y")
        self.points = points
        self.fouls = fouls
