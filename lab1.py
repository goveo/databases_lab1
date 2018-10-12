#  terminal:
#  pip install psycopg2-binary
#  sudo -u postgres psql
# \password

import datetime

from database import database
from models.musician import Musician
from models.release import Release
from models.listener import Listener

db = database.Database('127.0.0.1', 'postgres')
db.connect('postgres', '1')


patokaband = Musician(name='Patoka', members=["Skiper", "Kovalski", "Rico", "Private"])
sportsportsport = Musician(name='sportsportsport', members=["sportsman1", "sportsman2", "sportsman3"])
sports = Musician(name='sports', members=["sportsman1", "sportsman2", "sportsman3"])
release = Release(name='govno', date=datetime.datetime(year=1999, month=1, day=7))
girl14years = Listener(name='Anna Siryk', services=["soundcloud", "bandcamp"])
#
db.create_musicians_table()
db.create_releases_table()
db.create_listeners_table()

db.create_new_musician(patokaband)
db.create_new_musician(sportsportsport)
db.create_new_release(release, 1)
db.create_new_listener(girl14years, 1)
#
# sport_id = db.get_musician_by_name("sportsportsport")["id"]
# print(f'sport_id : {sport_id}')
# print(db.update_musician_by_id(sport_id, sports))

print(db.get_musician_id_by_name("Patoka"))
db.generate_random_releases(10)
db.generate_random_listeners(10)
# db.generate_random_listeners(10)

# db.get_all_musicians()

# print(db.get_musician_by_name("Patoka"))
