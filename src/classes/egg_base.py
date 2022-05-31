import datetime
import define as df


class EggBase:
    def __init__(self):
        self.id = None
        self.image = None
        self.name_en = None
        self.name_pt = None
        self.type_mob = False
        self.type_boss = False
        self.collected = False
        self.stars = 0
        self.find_normal_chapters = None
        self.find_hero_chapters = None
        self.find_events = None
        self.to_hatch = None
        self.natural_hatch = None
        self.quest1 = None
        self.quest1_unlocked = False
        self.quest2 = None
        self.quest2_unlocked = False
        self.train_cost = None
        self.train_stats = None
        self.train_stats_stars = None
        self.competition_available = False
        self.competition_stats = None
        self.date_created = None
        self.date_updated = None

        self.list_to_tuple = []
        self.sql_fields = []
        self.sql_values = ''

    def __str__(self):
        return f'id [{self.id}] ' \
               f'name_en [{self.name_en}] ' \
               f'mob [{self.type_mob}] ' \
               f'boss [{self.type_boss}] '

    def set_gen(self, **kwargs):
        if 'image' in kwargs:
            self.image = kwargs.get('image')
        if 'name_en' in kwargs:
            self.name_en = kwargs.get('name_en')
        if 'name_pt' in kwargs:
            self.name_pt = kwargs.get('name_pt')
        if 'type_mob' in kwargs:
            self.type_mob = kwargs.get('type_mob')
        if 'type_boss' in kwargs:
            self.type_boss = kwargs.get('type_boss')
        if 'collected' in kwargs:
            self.collected = kwargs.get('collected')
        if 'stars' in kwargs:
            self.stars = kwargs.get('stars')
        if 'find_normal_chapters' in kwargs:
            self.find_normal_chapters.value_orig = kwargs.get('find_normal_chapters')
        if 'find_hero_chapters' in kwargs:
            self.find_hero_chapters.value_orig = kwargs.get('find_hero_chapters')
        if 'find_events' in kwargs:
            self.find_events.value_orig = kwargs.get('find_events')
        if 'to_hatch' in kwargs:
            self.to_hatch = kwargs.get('to_hatch')
        if 'natural_hatch' in kwargs:
            self.natural_hatch = kwargs.get('natural_hatch')
        if 'quest1' in kwargs:
            self.quest1 = kwargs.get('quest1')
        if 'quest1_unlocked' in kwargs:
            self.quest1_unlocked = kwargs.get('quest1_unlocked')
        if 'quest2' in kwargs:
            self.quest2 = kwargs.get('quest2')
        if 'quest2_unlocked' in kwargs:
            self.quest2_unlocked = kwargs.get('quest2_unlocked')
        if 'train_cost' in kwargs:
            self.train_cost.value_orig = kwargs.get('train_cost')
        if 'train_stats' in kwargs:
            self.train_stats.value_orig = kwargs.get('train_stats')
        if 'train_stats_stars' in kwargs:
            self.train_stats_stars.value_orig = kwargs.get('train_stats_stars')
        if 'competition_available' in kwargs:
            self.competition_available = kwargs.get('competition_available')
        if 'competition_stats' in kwargs:
            self.competition_stats.value_orig = kwargs.get('competition_stats')
        if 'date_created' in kwargs:
            self.date_created = kwargs.get('date_created')
        if 'date_updated' in kwargs:
            self.date_updated = kwargs.get('date_updated')

    def get_fields(self, ignore_id=True):
        self.sql_fields = [
            'id',
            'image',
            'name_en',
            'name_pt',
            'type_mob',
            'type_boss',
            'collected',
            'stars',
            'find_normal_chapters',
            'find_hero_chapters',
            'find_events',
            'to_hatch',
            'natural_hatch',
            'quest1',
            'quest1_unlocked',
            'quest2',
            'quest2_unlocked',
            'train_cost',
            'train_stats',
            'train_stats_stars',
            'competition_available',
            'competition_stats',
            'date_created',
            'date_updated'
        ]
        sql_fields_tuple = tuple(self.sql_fields)
        if ignore_id:
            sql_fields_tuple = tuple(self.sql_fields[1:])

        self.sql_values = ''
        for _ in sql_fields_tuple:
            self.sql_values += '?,'

        return sql_fields_tuple, self.sql_values[:-1]

    def to_tuple_db(self):
        self.list_to_tuple = [
            self.image,
            self.name_en,
            self.name_pt,
            self.type_mob,
            self.type_boss,
            self.collected,
            self.stars,
            self.find_normal_chapters.value_orig,
            self.find_hero_chapters.value_orig,
            self.find_events.value_orig,
            self.to_hatch,
            self.natural_hatch,
            self.quest1,
            self.quest1_unlocked,
            self.quest2,
            self.quest2_unlocked,
            self.train_cost.value_orig,
            self.train_stats.value_orig,
            self.train_stats_stars.value_orig,
            self.competition_available,
            self.competition_stats.value_orig,
            self.date_created,
            self.date_updated,
        ]
        return tuple(self.list_to_tuple)

    def to_tuple_table(self):
        list_table = [self.name_en, self.get_type_desc(), self.stars]
        return tuple(list_table)

    def get_type_desc(self):
        desc = ''
        if self.type_mob:
            desc = 'Mob'
        elif self.type_boss:
            desc = 'Boss'
        return desc

    @staticmethod
    def conv_str2date(datetime_str=None):
        if datetime_str is None:
            return None
        datetime_obj = datetime.datetime.strptime(datetime_str, df.kDT_FORMAT2DATE)
        return datetime_obj

    @staticmethod
    def conv_date2str(datetime_obj=None):
        if datetime_obj is None:
            return ''
        datetime_str = datetime_obj.strftime(df.kDT_FORMAT2STRING)
        return datetime_str
