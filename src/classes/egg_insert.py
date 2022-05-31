import datetime
from classes.egg_base import EggBase
from classes.parser import *


class EggInsert(EggBase):
    def __init__(self):
        super(EggInsert, self).__init__()
        self.find_normal_chapters = FindParser(name='', value_orig=None)
        self.find_hero_chapters = FindParser(name='', value_orig=None)
        self.find_events = FindParser(name='', value_orig=None)
        self.train_cost = TrainCostParser(value_orig=None)
        self.train_stats = TrainStatParser(value_orig=None)
        self.train_stats_stars = TrainStatStarsParser(value_orig=None, egg_stars=0)
        self.competition_stats = CompetitionParser(value_orig=None)

        self.set_gen(date_created=datetime.datetime.now())

    def fill_example_mob(self, name):
        self.name_en = name
        self.type_mob = True

    def fill_example_boss(self, name):
        self.name_en = name
        self.type_boss = True
