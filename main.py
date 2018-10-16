#  terminal:
#  pip install psycopg2-binary
#  sudo -u postgres psql
# \password

import datetime
import npyscreen

from database.database import Database
from models.musician import Musician, Status
from models.release import Release
from models.listener import Listener
from tui import MainList
from tui import MusiciansList
from tui import MusicianEdit
from tui import ReleasesList
from tui import ReleaseEdit
from tui import ListenersList
from tui import ListenerEdit
from tui import SubscribeToRelease
from tui import SearchStatus
from tui import SearchVideo
from tui import FulltextSearch


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
        patokaband = Musician(name='Patoka',
                              status=Status.BAND.value,
                              members=["Skiper", "Kovalski", "Rico", "Private"])
        sportband = Musician(name='I love sport',
                             status=Status.BAND.value,
                             members=["Skiper", "Kovalski", "Rico", "Private"])
        sportsband = Musician(name='sports',
                              status=Status.ORCHESTRA.value,
                              members=["Skiper", "Kovalski", "Rico", "Private"])
        sportsportsport = Musician(name='sport sport sport',
                                   status=Status.BAND.value,
                                   members=["sportsman1", "sportsman2", "sportsman3"])
        release = Release(name='goveo',
                          date=datetime.datetime(year=1999, month=1, day=7),
                          style="emo",
                          is_video=True,
                          musician_id=1)
        release2 = Release(name='goveo2',
                           date=datetime.datetime(year=2018, month=1, day=7),
                           style="emo",
                           is_video=False,
                           musician_id=1)
        girl14years = Listener(name='Anna Siryk', services=["soundcloud", "bandcamp"])
        girl14years2 = Listener(name='Anna Siryk 2', services=["soundcloud", "bandcamp", "vk"])

        self.database.create_new_musician(patokaband)
        self.database.create_new_musician(sportband)
        self.database.create_new_musician(sportsband)
        self.database.create_new_musician(sportsportsport)
        self.database.create_new_release(release)
        self.database.create_new_release(release2)

        self.database.create_new_listener(girl14years)
        self.database.delete_listener_by_id(1)
        self.database.create_new_listener(girl14years2)
        self.database.add_listener_release(2, 1)
        self.database.add_listener_release(2, 2)

        # raise(Exception(self.database.full_text_musician_search('sports')))
        # raise(Exception(self.database.search_videos()))

        self.addForm("MAIN", MainList.MainListDisplay, title='Main menu')
        self.addForm("MUSICIANSLIST", MusiciansList.MusiciansListDisplay, title='Musicians')
        self.addForm("MUSICIANEDIT", MusicianEdit.MusicianEdit)
        self.addForm("RELEASESLIST", ReleasesList.ReleasesListDisplay)
        self.addForm("RELEASEEDIT", ReleaseEdit.ReleaseEdit)
        self.addForm("LISTENERSLIST", ListenersList.ListenersListDisplay)
        self.addForm("LISTENEREDIT", ListenerEdit.ListenerEdit)
        self.addForm("SUBSCRIBE_TO_RELEASE", SubscribeToRelease.SubscribeToRelease)
        self.addForm("SEARCH_STATUS", SearchStatus.SearchStatus)
        self.addForm("SEARCH_VIDEO", SearchVideo.SearchVideo)
        self.addForm("FULLTEXT_SEARCH", FulltextSearch.FulltextSearch)


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
