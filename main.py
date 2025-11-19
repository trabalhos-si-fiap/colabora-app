from src.populate_db.users import PopulateRawDB
from src.tui.login import ColaboraApp


def main():
    PopulateRawDB().run()
    ColaboraApp().run()


if __name__ == '__main__':
    main()
