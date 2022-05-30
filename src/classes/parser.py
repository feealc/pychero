
class ParserBase:
    def __init__(self, value_orig, parse_single=False, parse_double=False, parse_triple=False, type_last_param='bool'):
        self.main_char = '#'
        self.sub_char = ';'
        self.value_orig = value_orig
        self.value_parsed = []
        self.type_last_param = type_last_param

        if parse_single:
            self.__parse_single()
        elif parse_double:
            self.__parse_double()
        elif parse_triple:
            self.__parse_triple()

    def __parse_single(self):
        if self.value_orig is not None:
            self.value_parsed = self.value_orig.split(self.main_char)

    def __parse_double(self):
        aux_parse = []
        if self.value_orig is not None:
            aux_parse = self.value_orig.split(self.main_char)

        for aux in aux_parse:
            tmp = aux.split(self.sub_char)
            tmp2 = self.str_2_int(value_str=tmp[0])
            tmp3 = None
            if self.type_last_param == 'bool':
                tmp3 = self.str_2_bool(value_str=tmp[1])
            elif self.type_last_param == 'int':
                tmp3 = self.str_2_int(value_str=tmp[1])
            self.value_parsed.append((tmp2, tmp3))

    def __parse_triple(self):
        aux_parse = []
        if self.value_orig is not None:
            aux_parse = self.value_orig.split(self.main_char)

        for aux in aux_parse:
            tmp_split = aux.split(self.sub_char)
            tmp1 = self.str_2_int(value_str=tmp_split[0])
            tmp2 = tmp_split[1]
            tmp3 = self.str_2_int(value_str=tmp_split[2])
            self.value_parsed.append((tmp1, tmp2, tmp3))

    def dump(self):
        msg = (
            f'value_orig [{self.value_orig}] '
            f'value_parsed [{self.value_parsed}]'
        )
        print(msg)

    @staticmethod
    def str_2_bool(value_str):
        return True if value_str == 'True' else False

    @staticmethod
    def str_2_int(value_str):
        try:
            value_int = int(value_str)
        except ValueError:
            value_int = value_str
        return value_int


class FindParser(ParserBase):
    def __init__(self, name=None, value_orig=None):
        super().__init__(value_orig=value_orig, parse_double=True)
        self.name = name
        self.chapter_data = []

        self.parse()

    def parse(self):
        for ch in self.value_parsed:
            # print(f'value_split [{ch}]')
            ch_data = ChapterData(from_db=ch)
            self.chapter_data.append(ch_data)

    def dump_find(self, value_orig=False):
        print(f'Name [{self.name}]')
        for ch in self.chapter_data:
            print(ch)
        if value_orig:
            print(f'value_orig [{self.value_orig}]')

    def convert_to_db(self):
        if len(self.chapter_data) == 0:
            return None
        str_db = ''
        for ch in self.chapter_data:
            str_db += f'{ch.chapter}' + self.sub_char + f'{ch.recommended}'
            str_db += self.main_char
        # print(f'str_db [{str_db[:-1]}]')
        return str_db[:-1]

    def update(self, ch_data):
        for index, ch in enumerate(self.chapter_data):
            if ch.chapter == ch_data.chapter:
                self.chapter_data[index] = ch_data


class ChapterData:
    def __init__(self, from_db=None, from_add=None):
        self.chapter = 0
        self.recommended = False

        if from_db is not None:
            self.__parse(value=from_db)

        if from_add is not None:
            try:
                self.chapter = int(from_add[0])
            except ValueError:
                self.chapter = from_add[0]
            self.recommended = from_add[1]

    def __str__(self):
        return f'chapter [{self.chapter}] recommended [{self.recommended}]'

    @property
    def chapter_str(self):
        return str(self.chapter)

    def __parse(self, value):
        self.chapter = value[0]
        self.recommended = value[1]

    def get_recommended_desc(self):
        return 'Sim' if self.recommended else ''

    def to_tuple_table(self):
        lst = [self.chapter, self.get_recommended_desc()]
        return tuple(lst)


class TrainCostParser(ParserBase):
    def __init__(self, value_orig):
        super().__init__(value_orig=value_orig, parse_single=True)
        self.lst = self.value_parsed
        self.lst_int = []

        self.__convert_2_int()

    def __convert_2_int(self):
        for tc in self.value_parsed:
            self.lst_int.append(int(tc))

    def add_cost(self, value):
        self.lst.append(str(value))
        self.lst_int.append(value)
        self.sort()

    def sort(self):
        self.lst_int.sort()
        self.lst = map(str, self.lst_int)

    def convert_to_db(self):
        if len(self.lst) == 0:
            return None
        str_db = ''
        for tc in self.lst:
            str_db += f'{tc}'
            str_db += self.main_char
        # print(f'str_db [{str_db[:-1]}]')
        return str_db[:-1]

    def dump_tc_int(self):
        print(f'train_cost_list int {self.lst_int}')


class TrainStatParser(ParserBase):
    def __init__(self, value_orig):
        super().__init__(value_orig=value_orig, parse_double=True, type_last_param='int')
        self.train_stats_data = []

        self.__parse()

    def __parse(self):
        for value in self.value_parsed:
            # print(value)
            ts = TrainStatData(from_db=value)
            # print(ts)
            self.train_stats_data.append(ts)

    def add(self, data):
        self.train_stats_data.append(data)

    def dump(self):
        print(f'train_stats_data [{self.train_stats_data}]')

    def convert_to_db(self):
        if len(self.train_stats_data) == 0:
            return None
        str_db = ''
        for ts in self.train_stats_data:
            str_db += f'{ts.stat}{self.sub_char}{ts.stat_value}'
            str_db += self.main_char
        # print(f'str_db [{str_db[:-1]}]')
        return str_db[:-1]


class TrainStatData:
    def __init__(self, from_db=None, from_add=None):
        self.stat = None
        self.stat_value = None
        self.five_star = False

        if from_db is not None:
            self.__parse(value=from_db)

        if from_add is not None:
            self.stat = from_add[0]
            self.stat_value = from_add[1]
            self.five_star = from_add[2]

    def __str__(self):
        return f'stat [{self.stat}] stat_value [{self.stat_value}] 5s [{self.five_star}]'

    def __parse(self, value):
        aux = value[0]
        if aux.startswith('*'):
            self.stat = aux[1:]
            self.five_star = True
        else:
            self.stat = aux
        self.stat_value = value[1]

    def get_stat_table(self):
        if self.five_star:
            return '(5s)' + ' ' + self.stat
        else:
            return self.stat

    def to_tuple_table(self):
        lst = [self.get_stat_table(), self.stat_value]
        return tuple(lst)


class TrainStatStarsParser(ParserBase):
    def __init__(self, value_orig, egg_stars):
        super().__init__(value_orig=value_orig, parse_triple=True)
        self.train_stats_stars_data = []
        self.__egg_stars = egg_stars

        self.__parse()

    def __parse(self):
        for value in self.value_parsed:
            # print(value)
            tss = TrainStatStarsData(from_db=value, egg_stars=self.__egg_stars)
            # print(tss)
            self.train_stats_stars_data.append(tss)

    def add(self, data):
        self.train_stats_stars_data.append(data)
        self.__sort()

    def __sort(self):
        self.train_stats_stars_data.sort(key=lambda x: x.star)

    # def dump(self):
    #     print(f'train_stats_data [{self.train_stats_data}]')

    def convert_to_db(self):
        if len(self.train_stats_stars_data) == 0:
            return None
        str_db = ''
        for tss in self.train_stats_stars_data:
            str_db += f'{tss.star}' + self.sub_char + f'{tss.stat}' + self.sub_char + f'{tss.stat_value}'
            str_db += self.main_char
        # print(f'str_db [{str_db[:-1]}]')
        return str_db[:-1]


class TrainStatStarsData:
    def __init__(self, egg_stars, from_db=None, from_add=None):
        self.star = 0
        self.stat = None
        self.stat_value = None
        self.is_unlocked = False
        self.__egg_stars = egg_stars

        if from_db is not None:
            self.__parse(value=from_db)

        if from_add is not None:
            self.__parse(value=from_add)

    def __str__(self):
        return f'star [{self.star}] stat [{self.stat}] stat_value [{self.stat_value}] unlocked [{self.is_unlocked}] ' \
               f'star [{self.__egg_stars}]'

    def __parse(self, value):
        self.star = ParserBase.str_2_int(value_str=value[0])
        self.stat = value[1]
        self.stat_value = ParserBase.str_2_int(value_str=value[2])
        self.is_unlocked = self.__egg_stars >= self.star

    def get_is_unlocked(self):
        return '✅' if self.is_unlocked else ''

    def to_tuple_table(self):
        lst = [self.star, self.stat, self.stat_value, self.get_is_unlocked()]
        return tuple(lst)


class CompetitionParser(ParserBase):
    def __init__(self, value_orig):
        super().__init__(value_orig=value_orig, parse_double=True, type_last_param='int')
        self.competition_data = []

        self.__parse()

    def __parse(self):
        for value in self.value_parsed:
            # print(value)
            comp = CompetitionData(from_db=value)
            # print(comp)
            self.competition_data.append(comp)

    def add(self, data):
        self.competition_data.append(data)

    def convert_to_db(self):
        if len(self.competition_data) == 0:
            return None
        str_db = ''
        for comp in self.competition_data:
            str_db += f'{comp.stat}' + self.sub_char + f'{comp.stat_value}'
            str_db += self.main_char
        # print(f'str_db [{str_db[:-1]}]')
        return str_db[:-1]


class CompetitionData:
    def __init__(self, from_db=None, from_add=None):
        self.stat = None
        self.stat_value = None

        if from_db is not None:
            self.__parse(value=from_db)

        if from_add is not None:
            self.__parse(value=from_add)

    def __str__(self):
        return f'stat [{self.stat}] stat_value [{self.stat_value}]'

    def __parse(self, value):
        self.stat = value[0]
        self.stat_value = ParserBase.str_2_int(value_str=value[1])

    def to_tuple_table(self):
        lst = [self.stat, self.stat_value]
        return tuple(lst)
