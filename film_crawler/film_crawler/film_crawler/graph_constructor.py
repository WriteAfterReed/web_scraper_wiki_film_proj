import json


class Actor:

    def __init__(self, name="", year=1900, films=[], income=0):
        self.status = "actor"
        self.name = name
        self.year = year
        self.films = films
        self.income = income

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year

    def get_age(self):
        return 2019 - self.year

    def get_films(self):
        return self.films

    def add_film(self, film):
        self.films.append(film)

    def get_income(self):
        return self.income

    def add_income(self, income):
        self.income += income

    def get_status(self):
        return self.status


class Film:

    def __init__(self, name="", year=1900, cast=[], income=0):
        self.status = "film"
        self.name = name
        self.year = year
        self.cast = cast
        self.income = income

    def __str__(self):
        return self.name

    def get_status(self):
        return self.status

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year

    def get_cast(self):
        return self.cast

    def add_cast(self, actor):
        self.cast.append(actor)

    def get_income(self):
        return self.income

    def set_income(self, income):
        self.income = income


class Graph:

    def __init__(self):
        self.datum = {}

    def new_vert(self, node, entry=[]):
        self.datum[node] = entry

    def update_vert(self, node, entry):
        obj = self.datum[node]
        if entry not in obj:
            obj.append(entry)
        self.datum[node] = obj

    def get_verts(self):
        return self.datum.keys()

    def get_edges(self):
        return self.datum.values()

    def write_to_file(self):
        with open('result.json', 'w') as fp:
            json.dump(self.datum, fp)

    def read_from_json(self, path):
        dataset = None
        with open(path, 'r') as json_file:
            temp = json.load(json_file)
            self.datum = temp[0]

        count = 0
        print(type(self.datum))
        print(self.datum.keys())
        for each in self.datum:
            if count > 100:
                break
            print("")
            print(each)
            count += 1

def query_one(target, mapper):
    obj = mapper[target]
    gross = obj.get_income()
    print("Exec query 1...")
    print("For film: " + target + " the gross was: " + str(gross))
    print("Fin query 1 \n")


def query_two(target, mapper):
    obj = mapper[target]
    projects = obj.get_films()
    print("Exec query 2...")
    print("For Actor: " + target + " they have worked on:  " + str(projects))
    print("Fin query 2 \n")


def query_three(target, mapper):
    obj = mapper[target]
    team = obj.get_cast()
    print("Exec query 3...")
    print("For film: " + target + " the cast was: " + str(team))
    print("Fin query 3 \n")


def query_four(actor_map):
    payload = []
    for name in actor_map.keys():
        obj = actor_map[name]
        worth = obj.get_income()
        payload.append((name, worth))

    sorted_by_second = sorted(payload, key=lambda tup: tup[1])
    sorted_by_second.reverse()
    print("Exec query 4...")
    print("The top grossing actors are: ")
    for i in range(0, 5):
        entry = sorted_by_second[i]
        print(str(entry[0]) + " is worth " + str(entry[1]))
    print("Fin query 4 \n")


def query_five(actor_map):
    payload = []
    for name in actor_map.keys():
        obj = actor_map[name]
        age = obj.get_age()
        payload.append((name, age))

    sorted_by_second = sorted(payload, key=lambda tup: tup[1])
    sorted_by_second.reverse()
    print("Exec query 5...")
    print("The top oldest actors are: ")
    for i in range(0, 5):
        entry = sorted_by_second[i]
        print(str(entry[0]) + " is age " + str(entry[1]))
    print("Fin query 5 \n")


def query_six(film_map, target_year):
    payload = []
    print("Exec query 6...")
    print("For the year " + str(target_year) + " films are...")
    for movie in film_map.keys():
        obj = film_map[movie]
        film_year = obj.get_year()
        if film_year == target_year:
            print("Flim: " + movie)
    print("Fin query 6 \n")

def query_seven(actor_map, target_year):
    payload = []
    print("Exec query 7...")
    print("For the year " + str(target_year) + " actors born are...")
    for person in actor_map.keys():
        obj = actor_map[person]
        birth_year = obj.get_year()
        if birth_year == target_year:
            print("Actor: " + person)
    print("Fin query 7 \n")



actor_list = []
actor_dict = {}

film_list = []
film_dict = {}

graph = Graph()

graph.read_from_json("data.json")
def test_first_week():
    # dataset = None
    # with open('../out.json') as json_file:
    #     dataset = json.load(json_file)
    graph.read_from_json("data.json")
    #
    # for each in dataset:
    #     # This parses current Json for Actors
    #     if each['page_type'] == 'actor':
    #         year = each['actor_year']
    #         name = each['name']
    #         films = []
    #         income = 0
    #         if (2019 - year) > 100:
    #             continue
    #         if name not in actor_list:
    #             actor_list.append(name)
    #             new_actor = Actor(name, year, films, income)
    #             actor_dict[name] = new_actor
    #
    # for each in dataset:
    #
    #     # This parses current Json for films
    #     if each['page_type'] == "film":
    #         year = each['film_year']
    #         film_name = each['name']
    #         cast = each['film_cast']
    #         income = each['film_value']
    #         if film_name not in film_list:
    #             film_list.append(film_name)
    #             new_film = Film(film_name, year, cast, income)
    #             for person in cast:
    #                 if person in actor_dict.keys():
    #                     income = income // 2
    #                     actor_obj = actor_dict[person]
    #                     actor_obj.add_income(income)
    #                     actor_obj.add_film(film_name)
    #
    #             film_dict[film_name] = new_film
    #
    # for each in actor_list:
    #     entry = actor_dict[each]
    #     film_edges = entry.get_films()
    #     graph.new_vert(each, film_edges)
    #
    # for each in film_list:
    #     entry = film_dict[each]
    #     actor_edges = entry.get_cast()
    #     graph.new_vert(each, actor_edges)
    #
    # query_one("Drive (2011 film)", film_dict)
    # query_two("Michael Caine", actor_dict)
    # query_three("Drive (2011 film)", film_dict)
    # query_four(actor_dict)
    # query_five(actor_dict)
    # query_six(film_dict, 2012)
    # query_seven(actor_dict, 1964)
    #
    # graph.write_to_file()



