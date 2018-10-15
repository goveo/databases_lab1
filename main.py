#  terminal:
#  pip install psycopg2-binary
#  sudo -u postgres psql
# \password

import datetime
import npyscreen

from database.database import Database
from models.musician import Musician
from models.release import Release
from models.listener import Listener
from tui import MainList
from tui import MusiciansList
from tui import MusicianEdit
from tui import ReleasesList
from tui import ReleaseEdit


class MusiciansDBApp(npyscreen.NPSAppManaged):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.database = Database('127.0.0.1', 'postgres')

    def onStart(self):
        self.database.connect('postgres', '1')
        self.database.create_musicians_table()
        self.database.create_releases_table()
        self.database.create_listeners_table()
        self.database.create_listeners_releases_table()

        patokaband = Musician(name='Patoka', members=["Skiper", "Kovalski", "Rico", "Private"])
        sportsportsport = Musician(name='sportsportsport', members=["sportsman1", "sportsman2", "sportsman3"])
        release = Release(name='goveo', date=datetime.datetime(year=1999, month=1, day=7), style="emo", musician_id=1)
        release2 = Release(name='goveoLP', date=datetime.datetime(year=2018, month=1, day=7), style="emo", musician_id=1)
        girl14years = Listener(name='Anna Siryk', services=["soundcloud", "bandcamp"])

        self.database.create_new_musician(patokaband)
        self.database.create_new_musician(sportsportsport)
        self.database.create_new_release(release)
        self.database.create_new_release(release2)
        self.database.create_new_listener(girl14years)

        self.addForm("MAIN", MainList.MainListDisplay, title='Main menu')
        self.addForm("MUSICIANSLIST", MusiciansList.MusiciansListDisplay, title='Musicians')
        self.addForm("MUSICIANEDIT", MusicianEdit.MusicianEdit)
        self.addForm("RELEASESLIST", ReleasesList.ReleasesListDisplay)
        self.addForm("RELEASEEDIT", ReleaseEdit.ReleaseEdit)


    def onCleanExit(self):
        self.database.close()


if __name__ == '__main__':

    MyApp = MusiciansDBApp()
    MyApp.run()

    # db = Database('127.0.0.1', 'postgres')
    # db.connect('postgres', '1')

    # patokaband = Musician(name='Patoka', members=["Skiper", "Kovalski", "Rico", "Private"])
    # sportsportsport = Musician(name='sportsportsport', members=["sportsman1", "sportsman2", "sportsman3"])
    # sports = Musician(name='sports', members=["sportsman1", "sportsman2", "sportsman3"])
    # release = Release(name='govno', date=datetime.datetime(year=1999, month=1, day=7))
    # girl14years = Listener(name='Anna Siryk', services=["soundcloud", "bandcamp"])
    # #
    # db.create_musicians_table()
    # db.create_releases_table()
    # db.create_listeners_table()
    #
    # db.create_new_musician(patokaband)
    # db.create_new_musician(sportsportsport)
    # db.create_new_release(release, 1)
    # db.create_new_listener(girl14years, 1)
    # #
    # # sport_id = db.get_musician_by_name("sportsportsport")["id"]
    # # print(f'sport_id : {sport_id}')
    # # print(db.update_musician_by_id(sport_id, sports))
    #
    # print(db.get_musician_id_by_name("Patoka"))
    # db.generate_random_releases(10)
    # db.generate_random_listeners(10)
    # # db.generate_random_listeners(10)
    #
    # # db.get_all_musicians()
    #
    # # print(db.get_musician_by_name("Patoka"))
    #
    #
