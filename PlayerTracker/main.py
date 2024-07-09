from data_manager import DataManager
from app import Application
from core import Core


def main():
    data_manager = DataManager()
    core = Core(data_manager)
    app = Application(core)


if __name__ == '__main__':
    main()
