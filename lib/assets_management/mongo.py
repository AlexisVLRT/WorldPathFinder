import pymongo

from lib.credentials import credentials
from lib.misc.singleton import Singleton


@Singleton
class Mongo:
    def __init__(self):
        self.assets = None
        self.client = pymongo.MongoClient(
            host=credentials["mongo"]["host"],
            port=credentials["mongo"]["port"],
            username=credentials["mongo"]["username"],
            password=credentials["mongo"]["password"],
        )

    def get_checksums(self):
        return {
            file["filename"]: file["checksum_md5"]
            for file in self.client.blackfalcon.checksums.find({})
        }

    def get_doc(self, name):
        return self.client.blackfalcon.files.find_one({"filename": name})

    def get_all_docs(self):
        return self.client.blackfalcon.checksums.find({})
