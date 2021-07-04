import sqlite3
from sqlite3 import Error
from enum import Enum
from Clusters import Clusters

class Status(Enum):
    FREE = 0
    USED = 1
    COVID = 2
    EXAM = 3


class ClusterDB:
    def __init__(self, db_file=r"db/clusters.db"):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        
        self.clusters = ['oasis', 'illusion', 'mirage', 'atlantis']

        # atrium_table = """ CREATE TABLE IF NOT EXISTS atrium (
        # id integer PRIMARY KEY,
        # mac_id string,
        # is_vacant integer,
        # led_id integer,
        # status integer);"""

        oasis_table = """CREATE TABLE IF NOT EXISTS oasis (
        id integer PRIMARY KEY,
        mac_id string,
        # is_vacant integer,
        led_id integer,
        status integer);"""

        illusion_table = """CREATE TABLE IF NOT EXISTS illusion (
        id integer PRIMARY KEY,
        mac_id string,
        # is_vacant integer,
        led_id integer,
        status integer);"""

        mirage_table = """CREATE TABLE IF NOT EXISTS mirage (
        id integer PRIMARY KEY,
        mac_id string,
        # is_vacant integer,
        led_id integer,
        status integer);"""
    
        atlantis_table = """CREATE TABLE IF NOT EXISTS atlantis (
        id integer PRIMARY KEY,
        mac_id string,
        # is_vacant integer,
        led_id integer,
        status integer);"""
    
        if self.conn is not None:
            # self.create_table(atrium_table)
            self.create_table(oasis_table)
            self.create_table(illusion_table)
            self.create_table(mirage_table)
            self.create_table(atlantis_table)
            self.fill_clusters()

    def create_table(self, cmd):
        try:
            c = self.conn.cursor()
            c.execute(cmd)
        except Error as e:
            print(e)

    def delete_from_cluster(self, cluster, id):
        cmd = ''' DELETE FROM ''' + cluster + ''' WHERE user_id = ?'''

        cur = self.conn.cursor()
        cur.execute(cmd, (id,))
        self.conn.commit()

    def fetch_cluster_data(self, cluster, data):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM " + cluster)
        entries = cur.fetchall()
        for entry in entries:
            data.append(entry[1])
        return data

    def add_to_cluster(self, cluster, id):
        cmd = ''' INSERT INTO ''' + cluster + '''(mac_id) VALUES(?) '''
        cur = self.conn.cursor()

        cur.execute('SELECT * FROM ' + cluster + ' WHERE (mac_id=?)', (id,))
        entry = cur.fetchone()
        if entry is None:
            cur.execute(cmd, (id,))
            self.conn.commit()

        return cur.lastrowid
    
    def fill_clusters(self):
        for cluster in self.clusters:
            mac_ids = Clusters.get(cluster)
            for id in mac_ids:
                for i in range(1, id[1]+1):
                    self.add_to_cluster(cluster, id + i)

    # params = (status, mac_id)
    def change_mac_status(self, cluster, id, status):
        # check if status didn't change
        # return False in this case
        cmd = ''' INSERT INTO ''' + cluster + '''(status)
              VALUES(?) WHERE (mac_id=?)'''
        cur = self.conn.cursor()
        cur.execute(cmd, (status, id,))
        self.conn.commit()

        return True


    def delete_cluster(self, cluster):
        cmd = 'DELETE FROM ' + cluster
        cur = self.conn.cursor()
        cur.execute(cmd)
        self.conn.commit()

