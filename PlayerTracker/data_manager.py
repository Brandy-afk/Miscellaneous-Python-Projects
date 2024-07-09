import sqlite3
from player import Player

class DataManager:
    def __init__(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def insert_data(self, player: Player) -> bool:
        # Check if a player with the same first and last name already exists
        self.cursor.execute("SELECT * FROM players "
                            "WHERE first_name = ? "
                            "AND last_name = ?",
                            (player.first_name, player.last_name))
        existing_player = self.cursor.fetchone()

        if existing_player:
            # If a player with the same first and last name already exists, return False
            return False

        # Insert the new player into the database
        self.cursor.execute("INSERT INTO players (first_name, last_name, sport, team, number, position, date_added, points, fouls) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (player.first_name, player.last_name, player.sport, player.team, player.number, player.position, player.date_added, player.points, player.fouls))
        self.conn.commit()  # Commit the changes to the database
        return True

    def get_data(self, first_name: str, last_name: str) -> Player:
        # Retrieve a player from the database based on the first and last name
        self.cursor.execute("SELECT * FROM players "
                            "WHERE first_name = ? "
                            "AND last_name = ?",
                            (first_name, last_name))
        player_data = self.cursor.fetchone()

        if player_data:
            # If a player is found, create a Player object with the retrieved data
            player = Player(player_data[1], player_data[2], player_data[3], player_data[4], player_data[5],
                            player_data[6], player_data[8], player_data[9])
            player.date_added = player_data[7]
            return player
        else:
            # If no player is found, return None
            return None

    def update_data(self, player: Player, override: bool) -> bool:
        # Retrieve the existing player from the database
        existing_player = self.get_data(player.first_name, player.last_name)

        if existing_player:
            if override:
                # If override is True, update the existing player's data with the new data
                self.cursor.execute("UPDATE players SET sport = ?, team = ?, number = ?, position = ?, points = ?, fouls = ? "
                                    "WHERE first_name = ? "
                                    "AND last_name = ?",
                                    (player.sport, player.team, player.number, player.position, player.points, player.fouls, player.first_name, player.last_name))
            else:
                # If override is False, add the points and fouls to the existing player's data
                updated_points = existing_player.points + player.points
                updated_fouls = existing_player.fouls + player.fouls
                self.cursor.execute("UPDATE players SET points = ?, fouls = ? "
                                    "WHERE first_name = ? "
                                    "AND last_name = ?",
                                    (updated_points, updated_fouls, player.first_name, player.last_name))

            self.conn.commit()  # Commit the changes to the database
            return True
        else:
            # If the player doesn't exist, return False
            return False

    def delete_data(self, first_name: str, last_name: str) -> bool:
        # Delete a player from the database based on the first and last name
        self.cursor.execute("DELETE FROM players "
                            "WHERE first_name = ? "
                            "AND last_name = ?",
                            (first_name, last_name))
        deleted_rows = self.cursor.rowcount
        self.conn.commit()  # Commit the changes to the database

        # Return True if any rows were deleted, False otherwise
        return deleted_rows > 0