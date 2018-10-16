import psycopg2
import psycopg2.extras
import sys
import random
import string
import datetime
from models.musician import Musician, Status
from models.release import Release
from models.listener import Listener


class Database:
    def __init__(self, host, name):
        self.conn = None
        self.cur = None
        self.host = host
        self.name = name

    def connect(self, user, password):
        try:
            self.conn = psycopg2.connect(host=self.host, dbname=self.name, user=user, password=password)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            print('Error %s' % e)
            sys.exit(1)
        print('connected!')
        print(f' host : {self.host}')
        print(f' name : {self.name}')

    def close(self):
        self.cur.close()
        self.conn.close()

    #  region create table
    def create_musicians_table(self):
        statuses = Status.get_all()
        self.cur.execute(f"""DROP TYPE IF EXISTS status CASCADE""")
        self.cur.execute(f"""CREATE TYPE status AS 
                             ENUM ('{statuses[0]}', '{statuses[1]}', '{statuses[2]}', '{statuses[3]}');""")
        self.cur.execute("DROP TABLE IF EXISTS musicians CASCADE")
        self.cur.execute("""CREATE TABLE musicians(
                            id SERIAL PRIMARY KEY NOT NULL, 
                            name VARCHAR NOT NULL, 
                            status STATUS NOT NULL,
                            members VARCHAR[] NOT NULL)""")
        self.conn.commit()

    def create_releases_table(self):
        self.cur.execute("DROP TABLE IF EXISTS releases CASCADE")
        self.cur.execute("""CREATE TABLE releases(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            date DATE NOT NULL,
                            style VARCHAR NOT NULL,
                            isVideo BOOLEAN NOT NULL,
                            musicianId SERIAL NOT NULL,
                            FOREIGN KEY (musicianId) references musicians(id) 
                            ON DELETE CASCADE 
                            ON UPDATE CASCADE)""")
        self.conn.commit()

    def create_listeners_table(self):
        self.cur.execute("DROP TABLE IF EXISTS listeners CASCADE")
        self.cur.execute("""CREATE TABLE listeners(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            services VARCHAR[] NOT NULL,
                            releaseId SERIAL NOT NULL)""")
        self.conn.commit()

    def create_listeners_releases_table(self):
        self.cur.execute("DROP TABLE IF EXISTS listeners_releases")
        self.cur.execute("""CREATE TABLE listeners_releases(
                                    listenerId INTEGER,
                                    releaseId INTEGER,
                                    FOREIGN KEY (listenerId) references listeners(id),
                                    FOREIGN KEY (releaseId) references releases(id))""")
        self.conn.commit()
    #  endregion

    #  region create
    def create_new_musician(self, mus):
        self.cur.execute(f"""INSERT INTO musicians (name, members, status) 
                             VALUES ('{mus.name}', ARRAY{mus.members}, '{mus.status}')""")
        self.conn.commit()

    def create_new_release(self, release):
        self.cur.execute(f"""INSERT INTO releases (name, date, style, isVideo, musicianId) 
                             VALUES ('{release.name}', 
                                     '{release.date}', 
                                     '{release.style}',
                                     '{release.is_video}',
                                     '{release.musician_id}')""")
        self.conn.commit()

    def create_new_listener(self, listener):
        self.cur.execute(f"""INSERT INTO listeners (name, services) 
                             VALUES ('{listener.name}', ARRAY{listener.services})""")
        self.conn.commit()

    #  endregion

    #  region get all
    def get_all_musicians(self):
        self.cur.execute("SELECT * FROM musicians ORDER BY id")
        return self.cur.fetchall()

    def get_all_releases(self):
        self.cur.execute("SELECT * FROM releases ORDER BY id")
        return self.cur.fetchall()

    def get_all_listeners(self):
        self.cur.execute("SELECT * FROM listeners ORDER BY id")
        return self.cur.fetchall()

    #  endregion

    #  region get by name
    def get_musician_by_name(self, name):
        self.cur.execute(f"SELECT * FROM musicians WHERE name = '{name}'")
        try:
            return self.cur.fetchall()[0]
        except Exception as e:
            return False

    def get_release_by_name(self, name):
        self.cur.execute(f"SELECT * FROM releases WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    def get_listener_by_name(self, name):
        self.cur.execute(f"SELECT * FROM listeners WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    #  endregion

    #  region get by id
    def get_musician_by_id(self, id):
        self.cur.execute(f"SELECT * FROM musicians WHERE id = '{id}'")
        return self.cur.fetchone()

    def get_release_by_id(self, id):
        self.cur.execute(f"SELECT * FROM releases WHERE id = '{id}'")
        return self.cur.fetchone()

    def get_listener_by_id(self, id):
        self.cur.execute(f"SELECT * FROM listeners WHERE id = '{id}'")
        return self.cur.fetchone()

    #  endregion

    #  region update by id
    def update_musician_by_id(self, id, new_musician):
        self.cur.execute(f"""UPDATE musicians 
                             SET (name, status, members) = ('{new_musician.name}', 
                                                            '{new_musician.status}',
                                                             ARRAY{new_musician.members})
                             WHERE id = {id};""")
        self.conn.commit()

    def update_release_by_id(self, id, new_release):
        self.cur.execute(f"""UPDATE releases 
                             SET (name, date, style, isVideo, musicianId) = 
                             ('{new_release.name}', 
                              '{new_release.date}', 
                              '{new_release.style}', 
                              '{new_release.is_video}', 
                              '{new_release.musician_id}')
                             WHERE id = {id};""")
        self.conn.commit()

    def update_listener_by_id(self, id, new_listener):
        self.cur.execute(f"""UPDATE listeners 
                             SET (name, services) = ('{new_listener.name}', ARRAY{new_listener.services})
                             WHERE id = {id};""")
        self.conn.commit()

    #  endregion

    #  region delete by id
    def delete_musician_by_id(self, id):
        self.cur.execute(f"DELETE FROM musicians CASCADE WHERE id = '{id}';")
        self.conn.commit()

    def delete_release_by_id(self, id):
        self.cur.execute(f"DELETE FROM releases CASCADE WHERE id = '{id}';")
        self.conn.commit()

    def delete_listener_by_id(self, id):
        self.cur.execute(f"DELETE FROM listeners CASCADE WHERE id = '{id}';")
        self.conn.commit()

    #  endregion

    #   region get id by name
    def get_musician_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM musicians WHERE name = '{name}';")
        return self.cur.fetchone()[0]

    def get_release_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM releases WHERE name = '{name}';")
        return self.cur.fetchone()[0]

    def get_listener_id_by_name(self, name):
        self.cur.execute(f"SELECT id FROM listeners WHERE name = '{name}';")
        return self.cur.fetchone()[0]
    #   endregion

    #   region generate random data
    def generate_random_musicians(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            status = random.choice(Status.get_all())
            number_of_members = random.randint(1, 4)
            members = []
            for j in range(number_of_members):
                band_name = self.__generate_random_string(3, 12)
                members.append(band_name)
            musician = Musician(name=name, status=status, members=members)
            self.create_new_musician(musician)

    def generate_random_releases(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            date = self.__generate_random_date()
            style = self.__generate_random_string(3, 12)
            is_video = random.choice([True, False])
            musician_count = self.get_musicians_count()
            musician_id = random.randint(1, musician_count)
            release = Release(name, date, style, is_video, musician_id)
            self.create_new_release(release)

    def generate_random_listeners(self, num: int):
        for i in range(num):
            name = self.__generate_random_string(3, 12)
            number_of_services = random.randint(1, 4)
            services = []
            for j in range(number_of_services):
                band_name = self.__generate_random_string(3, 12)
                services.append(band_name)
            listener = Listener(name, services)
            releases_count = self.get_releases_count()
            release_id = random.randint(1, releases_count)
            self.create_new_listener(listener, release_id)

    #   endregion

    def add_listener_release(self, listener_id, release_id):
        self.cur.execute(f"""INSERT INTO listeners_releases (listenerId, releaseId) 
                             VALUES ('{listener_id}', '{release_id}')""")
        self.conn.commit()

    def get_listeners_id_by_release_id(self, release_id):
        self.cur.execute(f"SELECT listenerid FROM listeners_releases WHERE releaseId = '{release_id}'")
        return self.cur.fetchall()

    def get_releases_id_by_listener_id(self, listener_id):
        self.cur.execute(f"SELECT releaseid FROM listeners_releases WHERE listenerId = '{listener_id}'")
        return self.cur.fetchall()

    def get_releases_by_listener_id(self, listener_id):
        releases_id = self.get_releases_id_by_listener_id(listener_id)
        data = []
        for i in releases_id:
            data.append(self.get_release_by_id(i[0]))
        return data

    def update_all_subscriptions_by_listener_id(self, listener_id, releases_id):
        self.cur.execute(f"DELETE FROM listeners_releases WHERE listenerId = '{listener_id}'")
        for release_id in releases_id:
            self.cur.execute(f"""INSERT INTO listeners_releases (listenerId, releaseId) 
                                         VALUES ('{listener_id}', '{release_id}')""")
        self.conn.commit()

    def get_musicians_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM musicians;")
        return self.cur.fetchone()

    def get_releases_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM releases;")
        return self.cur.fetchone()[0]

    def get_listeners_count(self):
        self.cur.execute(f"SELECT COUNT (*) FROM listeners;")
        return self.cur.fetchone()[0]

    def get_count_of_an_entity(self, entity):
        entity = entity.lower()
        if entity == "musicians":
            return self.get_musicians_count()
        elif entity == "releases":
            return self.get_releases_count()
        elif entity == "listeners":
            return self.get_listeners_count()
        else:
            return 0



    @staticmethod
    def __generate_random_string(min: int, max: int):
        s = string.ascii_letters
        return ''.join(random.sample(s, random.randint(min, max)))

    @staticmethod
    def __generate_random_date():
        year = random.randint(1950, 2018)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return datetime.datetime(year, month, day)

    def full_text_musician_search(self, query):
        self.cur.execute(f"""SELECT * FROM musicians WHERE to_tsvector(name) @@ plainto_tsquery('{query}')""")
        return self.cur.fetchall()

    def search_videos(self, query: bool):
        self.cur.execute(f"""SELECT * FROM releases WHERE isVideo = '{query}'""")
        return self.cur.fetchall()

    def search_status(self, status: Status):
        self.cur.execute(f"""SELECT * FROM musicians WHERE status = '{status}'""")
        return self.cur.fetchall()