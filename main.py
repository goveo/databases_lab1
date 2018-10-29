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
        self.fill_database()

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

    def fill_database(self):
        self.database.create_musicians_table()
        self.database.create_releases_table()
        self.database.create_listeners_table()
        self.database.create_listeners_releases_table()

        patokaband = Musician(name='Patoka',
                              status=Status.BAND.value,
                              members=["Skiper", "Kovalski", "Rico"])
        sportband = Musician(name='Lets sport',
                             status=Status.BAND.value,
                             members=["Skiper", "Kovalski", "Private"])
        sportsband = Musician(name='sports',
                              status=Status.ORCHESTRA.value,
                              members=["Skiper", "Kovalski", "Rico", "Private"])
        sportsportsport = Musician(name='sport sport sport',
                                   status=Status.BAND.value,
                                   members=["sportsman1", "sportsman2", "sportsman3"])
        release1 = Release(name='Release1',
                          date=datetime.datetime(year=1999, month=1, day=7),
                          style="Pop",
                          is_video=True,
                          musician_id=3)
        release2 = Release(name='Release2',
                           date=datetime.datetime(year=2018, month=1, day=7),
                           style="Garage rock",
                           is_video=False,
                           musician_id=1)
        release3 = Release(name='Release3',
                           date=datetime.datetime(year=2018, month=1, day=7),
                           style="Rock",
                           is_video=False,
                           musician_id=3)
        listener1 = Listener(name='Anna Siryk', services=["soundcloud", "bandcamp"])
        listener2 = Listener(name='Simple Listener', services=["soundcloud", "vk"])
        listener3 = Listener(name='Listener3', services=["soundcloud"])

        self.database.create_new_musician(patokaband)
        self.database.create_new_musician(sportband)
        self.database.create_new_musician(sportsband)
        self.database.create_new_musician(sportsportsport)
        # self.database.generate_random_musicians(100)

        self.database.create_new_release(release1)
        self.database.create_new_release(release2)
        self.database.create_new_release(release3)

        self.database.create_new_listener(listener1)
        self.database.create_new_listener(listener2)
        self.database.create_new_listener(listener3)

        self.database.add_listener_release(1, 1)
        self.database.add_listener_release(2, 1)
        self.database.add_listener_release(1, 2)

if __name__ == '__main__':

    MyApp = MusiciansDBApp()
    MyApp.run()

