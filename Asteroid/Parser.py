__author__ = 'Kirill Kononov, Sergey Karashevich'

import re, os, psycopg2
from os.path import join

class Parser:

    def __init__(self, proclogFileName):
        self.proclog = list()
        self.info = dict()
        self.info["CAT_ASTR"] = 'empty'
        self.info["CCD_TEMP"] = 'empty'
        self.info["FILTER"] = 'empty'
        self.info["IMG_CENTER_RA"] = 'empty'
        self.info["IMG_CENTER_DEC"] = 'empty'
        self.info["LONG"] = 'empty'
        self.info["LAT"] = 'empty'
        self.info["ALT"] = 'empty'

        with open(proclogFileName, 'r') as input_file:
            for line in input_file:
                self.proclog.append(line)

    def parse(self, info_prefix, info_id, info_postfix):
        for line in self.proclog:
            name_prefix = re.search(info_prefix + "\s*", line)

            if name_prefix:
                name = line[name_prefix.end(): line.find(info_postfix, name_prefix.end())]
                self.info[info_id] = name

                return

    def printParser(self):
        print(self.info)

    def fillDict(self):
        self.parse("Processing image \"", "IMG_NAME", "\"")
        self.parse("Exposure duration:", "EXPOSURE", "\n")
        self.parse("CCD temperature =", "CCD_TEMP", "K")
        self.parse("filter \"", "FILTER", "\"")
        self.parse("Observation target:", "OBJECT", "\n")

        if self.info.get("OBJECT") is None:
            return

        self.info["DESIGNATED"] = re.sub(r'\W', '', self.info.get("OBJECT"))
        self.parse("Mid-exposure time:", "EXPTIME", "UTC")
        self.parse("Latitude:", "LAT", "\n")
        self.parse("Longitude:", "LONG", "\n")
        self.parse("Altitude:", "ALT", "m")
        self.parse("Reference catalog:", "CAT_ASTR", "\n")
        self.parse("Image center RA", "IMG_CENTER_RA", "  ")
        self.parse("Image center Dec", "IMG_CENTER_DEC", "  ")

    def process(self):
        self.fillDict()
        if self.info.get("OBJECT") is not None:
            self.add_to_database()

    def add_to_database(self):
        conn = psycopg2.connect("dbname='asteroidb' user='postgres' host='localhost' password='superpass'")
        cur = conn.cursor()

        d = self.info

        # adding new asteroid to DB
        ast_name = d.get("OBJECT")
        cur.execute("SELECT id  FROM proclogs_asteroidobs WHERE object_name = '" + ast_name +"';")
        k = cur.fetchone()
        if k is None:
            cur.execute("INSERT INTO proclogs_asteroidobs (object_name, designated_name) VALUES (%s, %s)",
                (ast_name, re.sub(r'\W', '', ast_name)))

            cur.execute("SELECT id  FROM proclogs_asteroidobs WHERE object_name = '" + ast_name +"';")
            k = cur.fetchone()
            conn.commit()

        # adding new proclog to DB
        image_name = d.get("IMG_NAME")
        cur.execute("SELECT id  FROM proclogs_proclog WHERE pclg_image_name = '" + image_name +"';")
        l = cur.fetchone()
        if l is None:
            cur.execute("INSERT INTO proclogs_proclog (observation_id, pclg_image_name, pclg_exposure, \"pclg_CCD_temp\","
                        " pclg_filter, pclg_exp_time, pclg_latitude, "
                        "pclg_longitude, pclg_altitude, pclg_catalog_astrometric,"
                        " \"pclg_image_center_RA\", \"pclg_image_center_DEC\") VALUES (" + str(k[0]) + ", %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )",
                ( d.get("IMG_NAME"),d.get("EXPOSURE"), d.get("CCD_TEMP"),
                  d.get("FILTER"), d.get("EXPTIME"), d.get("LAT"),
                  d.get("LONG"), d.get("ALT"), d.get("CAT_ASTR"),
                  d.get("IMG_CENTER_RA"), d.get("IMG_CENTER_DEC")))

        conn.commit()

        # closing connections
        cur.close()
        conn.close()


def isProclog(line):
    if line.endswith(".proclog"):
        return True
    else:
        return False


def main():
    for root, dirs, files in os.walk("."):
        for name in files:
            if isProclog(name):
                print (join(root, name))
                parser = Parser(join(root, name))
                parser.process()
                del parser

main()