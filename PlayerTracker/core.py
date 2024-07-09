from data_manager import DataManager
from player import Player


class Core:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def add_player(self, player: Player) -> bool:
        return self.data_manager.insert_data(player)

    def get_player(self, first_name: str, last_name: str) -> Player:
        return self.data_manager.get_data(first_name, last_name)

    def update_player(self, player: Player, override: bool) -> bool:
        return self.data_manager.update_data(player, override)

    def delete_player(self, first_name: str, last_name: str) -> bool:
        return self.data_manager.delete_data(first_name, last_name)
