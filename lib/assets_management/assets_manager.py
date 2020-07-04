import json
import os
import time
import hashlib
from pathlib import Path
from multiprocessing import Pool, cpu_count

from lib.assets_management.mongo import Mongo
from lib.misc.singleton import Singleton


@Singleton
class Assets:
    def __init__(self):
        self.assets_filter = ["map_info", "pathfinder_graph"]
        self.assets_paths = Path(__file__).parent.parent.parent / "assets"
        self.mongo = Mongo.instance()
        self.mongo.assets = self
        self.assets = {}
        self.load_assets()

    def load_assets(self):
        start = time.time()
        self.update_assets()
        files_packs = {}
        print("Mapping static assets")
        for file in os.listdir(self.assets_paths):
            if file.endswith(".json"):
                if file.replace(".json", "").split("_")[-1].isdigit():
                    if (
                        "_".join(file.replace(".json", "").split("_")[:-1])
                        not in files_packs.keys()
                    ):
                        files_packs[
                            "_".join(file.replace(".json", "").split("_")[:-1])
                        ] = [file]
                    else:
                        files_packs[
                            "_".join(file.replace(".json", "").split("_")[:-1])
                        ].append(file)
                else:
                    files_packs[file.replace(".json", "")] = [file]

        print("Loading static assets...")
        self.load_assets_list(files_packs)
        print("Done loading assets in {}s".format(round(time.time() - start, 2)))

    def load_assets_list(self, files_packs):
        for asset_name, file_pack in files_packs.items():
            print("Loading asset: {}".format(asset_name))
            if len(file_pack) <= 20:
                for file in file_pack:
                    with open(self.assets_paths / file, "r", encoding="utf8") as f:
                        data = json.load(f)
                    if asset_name not in self.assets.keys():
                        self.assets[asset_name] = data
                    else:
                        if type(data) is list:
                            self.assets[asset_name] += data
                        elif type(data) is dict:
                            self.assets[asset_name].update(data)
            else:
                with Pool(cpu_count() - 1) as p:
                    results_list = p.map(
                        self.load_asset_chunk,
                        [
                            self.assets_paths + "/" + file_name
                            for file_name in file_pack
                        ],
                    )
                for asset_chunk in results_list:
                    if asset_name not in self.assets.keys():
                        self.assets[asset_name] = asset_chunk
                    else:
                        if type(asset_chunk) is list:
                            self.assets[asset_name] += asset_chunk
                        elif type(asset_chunk) is dict:
                            self.assets[asset_name].update(asset_chunk)

    def load_asset_chunk(self, file_path):
        with open(file_path, "r", encoding="utf8") as f:
            chunk = json.load(f)
        return chunk

    def update_assets(self):
        self.remove_deprecated_assets()

        mongo_checksums = self.mongo.get_checksums(files_filter=self.assets_filter)
        local_checksums = self.create_assets_checksums()

        files_to_update = get_files_to_update(mongo_checksums, local_checksums)

        [self.download_file(filename) for filename in files_to_update]
        print("All files are up to date")
        return files_to_update

    def create_assets_checksums(self):
        checksums = {}
        for file in os.listdir(self.assets_paths):
            if file.endswith(".json"):
                checksums[file.replace(".json", "")] = generate_file_md5(
                    self.assets_paths / file
                )
        return checksums

    def remove_deprecated_assets(self):
        local_files = set(
            [
                path.replace(".json", "")
                for path in os.listdir(self.assets_paths)
                if path.endswith(".json")
            ]
        )
        mongo_files = set(
            [
                document["filename"]
                for document in self.mongo.get_all_docs()
            ]
        )
        files_to_remove = local_files - mongo_files
        for file in files_to_remove:
            print("Removing deprecated local file", file)
            os.remove(self.assets_paths / (file + ".json"))

    def download_file(self, filename):
        print("Downloading " + filename)
        data = self.mongo.get_doc(filename)
        with open(self.assets_paths / (filename + ".json"), "w", encoding="utf8") as f:
            json.dump(data["payload"], f, ensure_ascii=False)


def generate_file_md5(path, blocksize=2 ** 20):
    m = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def get_files_to_update(mongo_checksums, local_checksums):
    files_to_update = []
    for filename, checksum in mongo_checksums.items():
        if (
            not filename in local_checksums.keys()
            or checksum != local_checksums[filename]
        ):
            print("Checksum doesn't match for", filename)
            files_to_update.append(filename)
    return files_to_update

