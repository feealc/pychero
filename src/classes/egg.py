from classes.egg_base import EggBase
from classes.parser import *
from database.archero_db import ArcheroDb
import define as df


class Egg(EggBase):
    def __init__(self, tuple_from_db=None):
        super(Egg, self).__init__()
        self.fields = None
        if tuple_from_db is not None:
            self.__parse(tuple_from_db=tuple_from_db)

    def __parse(self, tuple_from_db):
        index = 0
        self.id = tuple_from_db[index]

        index += 1
        self.image = None

        index += 1
        self.name_en = tuple_from_db[index]

        index += 1
        self.name_pt = tuple_from_db[index]

        index += 1
        self.type_mob = bool(tuple_from_db[index])

        index += 1
        self.type_boss = bool(tuple_from_db[index])

        index += 1
        self.collected = bool(tuple_from_db[index])

        index += 1
        self.stars = tuple_from_db[index]

        index += 1
        self.find_normal_chapters = FindParser(name=df.kNORMAL_CHAPTER, value_orig=tuple_from_db[index])
        # self.find_normal_chapters.dump()
        # self.find_normal_chapters.dump_find()

        index += 1
        self.find_hero_chapters = FindParser(name=df.kHERO_CHAPTER, value_orig=tuple_from_db[index])
        # self.find_hero_chapters.dump()
        # self.find_hero_chapters.dump_find()

        index += 1
        self.find_events = FindParser(name=df.kEVENT, value_orig=tuple_from_db[index])
        # self.find_events.dump()
        # self.find_events.dump_find()

        index += 1
        self.to_hatch = tuple_from_db[index]

        index += 1
        self.natural_hatch = tuple_from_db[index]

        index += 1
        self.quest1 = tuple_from_db[index]

        index += 1
        self.quest1_unlocked = bool(tuple_from_db[index])

        index += 1
        self.quest2 = tuple_from_db[index]

        index += 1
        self.quest2_unlocked = bool(tuple_from_db[index])

        index += 1
        self.train_cost = TrainCostParser(value_orig=tuple_from_db[index])
        # self.train_cost.dump()
        # self.train_cost.dump_tc_int()

        index += 1
        self.train_stats = TrainStatParser(value_orig=tuple_from_db[index])

        index += 1
        self.train_stats_stars = TrainStatStarsParser(value_orig=tuple_from_db[index], egg_stars=self.stars)

        index += 1
        self.competition_available = bool(tuple_from_db[index])

        index += 1
        self.competition_stats = CompetitionParser(value_orig=tuple_from_db[index])
        # self.competition_stats.dump()

    @property
    def to_hatch_str(self):
        return '' if self.to_hatch is None else str(self.to_hatch)

    @property
    def natural_hatch_str(self):
        return '' if self.natural_hatch is None else str(self.natural_hatch)

    @property
    def quest1_str(self):
        return '' if self.quest1 is None else str(self.quest1)

    @property
    def quest2_str(self):
        return '' if self.quest2 is None else str(self.quest2)

    def dump(self):
        msg = (
            '\n' +
            f'>>> id [{self.id}] name_en [{self.name_en}] name_pt [{self.name_pt}]' + '\n'
            # f'image [{self.image}]' + '\n'
            f'type_mob [{self.type_mob}] type_boss [{self.type_boss}]' + '\n'
            f'collected [{self.collected}] stars [{self.stars}]' + '\n'
            f'fnc [{self.find_normal_chapters.value_orig}] fhc [{self.find_hero_chapters.value_orig}] ' +
            f'fe [{self.find_events.value_orig}]' + '\n'
            f'to_hatch [{self.to_hatch}] natural_hatch [{self.natural_hatch}]' + '\n'
            f'quest1 [{self.quest1}] quest1_unlocked [{self.quest1_unlocked}]' + '\n'
            f'quest2 [{self.quest2}] quest2_unlocked [{self.quest2_unlocked}]' + '\n'
            f'train_cost [{self.train_cost.value_orig}]' + '\n'
            f'train_stats [{self.train_stats.value_orig}]' + '\n'
            f'train_stats_stars [{self.train_stats_stars.value_orig}]' + '\n'
            f'competition_available [{self.competition_available}] '
            f'competition_stats [{self.competition_stats.value_orig}]'
        )
        print(msg)

    def find_chapter_exists(self, title, chapter) -> bool:
        if title == df.kNORMAL_CHAPTER:
            for ch in self.find_normal_chapters.chapter_data:
                if int(chapter) == ch.chapter:
                    return True
        elif title == df.kHERO_CHAPTER:
            for ch in self.find_hero_chapters.chapter_data:
                if int(chapter) == ch.chapter:
                    return True
        elif title == df.kEVENT:
            for ch in self.find_events.chapter_data:
                if chapter == ch.chapter:
                    return True
        return False

    def add_chapter(self, title, ch_data):
        if not self.find_chapter_exists(title=title, chapter=ch_data.chapter):
            if title == df.kNORMAL_CHAPTER:
                self.find_normal_chapters.chapter_data.append(ch_data)
            elif title == df.kHERO_CHAPTER:
                self.find_hero_chapters.chapter_data.append(ch_data)
            elif title == df.kEVENT:
                self.find_events.chapter_data.append(ch_data)
            self.sort_chapter_data()
            return True
        else:
            return False

    def update_chapter(self, title, ch_data):
        if title == df.kNORMAL_CHAPTER:
            self.find_normal_chapters.update(ch_data=ch_data)
        elif title == df.kHERO_CHAPTER:
            self.find_hero_chapters.update(ch_data=ch_data)
        elif title == df.kEVENT:
            self.find_events.update(ch_data=ch_data)

        self.sort_chapter_data()

    def sort_chapter_data(self):
        self.find_normal_chapters.chapter_data.sort(key=lambda x: x.chapter)
        self.find_hero_chapters.chapter_data.sort(key=lambda x: x.chapter)
        self.find_events.chapter_data.sort(key=lambda x: x.chapter)

    def update_fields(self):
        db = ArcheroDb()
        cols = db.list_columns_from_table(table_name='EGGS')
        self.fields = ''
        for index, col in enumerate(cols):
            if index > 0:  # ignore 'id'
                self.fields += col + ' = ?, '
        return self.fields[:-2]
