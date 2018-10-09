import psycopg2
import psycopg2.extras
import sys


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

    # def drop(self):
        # self.cur.execute(f" DROP TABLE *")
        # print('Dropped!')

    def create_musicians_table(self):
        self.cur.execute("DROP TABLE IF EXISTS musicians CASCADE")
        self.cur.execute("""CREATE TABLE musicians(
                            id SERIAL PRIMARY KEY NOT NULL, 
                            name VARCHAR NOT NULL, 
                            members VARCHAR[] NOT NULL)""")

    def create_releases_table(self):
        self.cur.execute("DROP TABLE IF EXISTS releases CASCADE")
        self.cur.execute("""CREATE TABLE releases(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            date DATE NOT NULL,
                            musicianId SERIAL NOT NULL,
                            FOREIGN KEY (musicianId) references musicians(id))""")

    def create_listeners_table(self):
        self.cur.execute("DROP TABLE IF EXISTS listeners")
        self.cur.execute("""CREATE TABLE listeners(
                            id SERIAL PRIMARY KEY, 
                            name VARCHAR NOT NULL, 
                            services VARCHAR[] NOT NULL,
                            listenerId SERIAL NOT NULL,
                            FOREIGN KEY (listenerId) references releases(id))""")

    def create_new_musician(self, mus):
        self.cur.execute(f"INSERT INTO musicians (name, members) VALUES ('{mus.name}', ARRAY{mus.members})")
        self.conn.commit()

    def create_new_release(self, release):
        self.cur.execute(f"INSERT INTO releases (name, date) VALUES ('{release.name}', '{release.date}')")
        self.conn.commit()

    def create_new_listener(self, listener):
        self.cur.execute(f"INSERT INTO listeners (name, services) VALUES ('{listener.name}', ARRAY{listener.services})")
        self.conn.commit()

    def get_all_musicians(self):
        self.cur.execute("SELECT * FROM musicians")
        return self.cur.fetchall()

    def get_all_releases(self):
        self.cur.execute("SELECT * FROM releases")
        return self.cur.fetchall()

    def get_all_listeners(self):
        self.cur.execute("SELECT * FROM listener")
        return self.cur.fetchall()

    def get_musician_by_name(self, name):
        self.cur.execute(f"SELECT * FROM musicians WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    def get_release_by_name(self, name):
        self.cur.execute(f"SELECT * FROM releases WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    def get_listener_by_name(self, name):
        self.cur.execute(f"SELECT * FROM listener WHERE name = '{name}'")
        return self.cur.fetchall()[0]

    def get_musician_by_id(self, id):
        self.cur.execute(f"SELECT * FROM musician WHERE id = '{id}'")
        return self.cur.fetchone()[0]

    def get_release_by_id(self, id):
        self.cur.execute(f"SELECT * FROM releases WHERE id = '{id}'")
        return self.cur.fetchone()[0]

    def get_listener_by_id(self, id):
        self.cur.execute(f"SELECT * FROM listener WHERE id = '{id}'")
        return self.cur.fetchone()[0]

    def update_musician_by_id(self, id, new_musician):
        self.cur.execute(f"""UPDATE musicians SET (name, members) = ('{new_musician.name}', ARRAY{new_musician.members})
                             WHERE id = {id};""")
        self.conn.commit()

    def update_release_by_id(self, id, new_release):
        self.cur.execute(f"""UPDATE releases SET (name, date) = ('{new_release.name}', '{new_release.date}')
                             WHERE id = {id};""")
        self.conn.commit()

    def update_listener_by_id(self, id, new_listener):
        self.cur.execute(f"""UPDATE releases SET (name, services) = ('{new_listener.name}', ARRAY{new_listener.services})
                             WHERE id = {id};""")
        self.conn.commit()