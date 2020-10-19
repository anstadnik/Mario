from menu import Menu
from ipdb import launch_ipdb_on_exception


def main():
    game = Menu(1280, 720)
    with launch_ipdb_on_exception():
        game.run()


if __name__ == "__main__":
    main()
