import json


class HandleJson:
    def __init__(self, file_name):
        self.__file_json = None
        self.__file_name = file_name

        self.__load_file()

    def __load_file(self):
        with open(self.__file_name, 'r', encoding='utf-8') as f:
            self.__file_json = json.load(f)

    def dump_json(self):
        print(json.dumps(self.__file_json, indent=4, ensure_ascii=False))

    def get_file(self):
        return self.__file_json

    def reload_file(self):
        self.__load_file()

    def get_chapter_min(self):
        return self.__file_json['chapters']['min']

    def get_chapter_max(self):
        return self.__file_json['chapters']['max']

    def get_events(self):
        return self.__file_json['events']

    def get_stars_min(self):
        return self.__file_json['stars']['min']

    def get_stars_max(self):
        return self.__file_json['stars']['max']

    def get_train_stats(self):
        return self.__file_json['train_stats']
