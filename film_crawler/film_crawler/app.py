from flask import Flask
import json
from flask import jsonify
from flask import request
from flask import abort
import operator
import matplotlib.pyplot as plt
import math

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
datum = {}
global_actors = {}


@app.route('/')
def index():
    return "Hello, World!"


@app.route("/actors", methods=['GET'])
def filter_actor():
    attr1 = None
    attr2 = None
    out = {}

    attr_value = request.args.get('name')
    attr_value = attr_value.replace("'", "")
    attr_value = attr_value.replace("\"", "")

    or_loc = attr_value.find("|")
    and_loc = attr_value.find("&")
    if or_loc != -1:
        attr1 = attr_value[0:or_loc]
        attr2 = attr_value[or_loc + 1: len(attr_value)]
        for each in datum.keys():
            if attr1 in each or attr2 in each:
                out[attr_value] = datum[each]
        return jsonify(out)

    if and_loc != -1:
        attr1 = attr_value[0:or_loc]
        attr2 = attr_value[or_loc + 1: len(attr_value)]
        for each in datum.keys():
            if attr1 in each and attr2 in each:
                out[attr_value] = datum[each]
        return jsonify(out)

    for each in datum.keys():
        if attr_value in each:
            out[attr_value] = datum[each]

    return jsonify(out)


@app.route("/movies", methods=['GET'])
def filter_movie():
    attr1 = None
    attr2 = None
    out = {}

    attr_value = request.args.get('name')
    attr_value = attr_value.replace("'", "")
    attr_value = attr_value.replace("\"", "")

    or_loc = attr_value.find("|")
    and_loc = attr_value.find("&")
    if or_loc != -1:
        attr1 = attr_value[0:or_loc]
        attr2 = attr_value[or_loc + 1: len(attr_value)]
        for each in datum.keys():
            if attr1 in each or attr2 in each:
                out[attr_value] = datum[each]
        return jsonify(out)

    if and_loc != -1:
        attr1 = attr_value[0:or_loc]
        attr2 = attr_value[or_loc + 1: len(attr_value)]
        for each in datum.keys():
            if attr1 in each and attr2 in each:
                out[attr_value] = datum[each]
        return jsonify(out)

    for each in datum.keys():
        if attr_value in each:
            out[attr_value] = datum[each]

    return jsonify(out)


@app.route("/actors/<name>", methods=['GET'])
def get_actor(name):
    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    out = None
    if name not in datum.keys():
        return "404 Not Found"
    for each in datum.keys():
        if name == each:
            out = datum[each]
            break
    return jsonify(out)


@app.route("/movies/<name>", methods=['GET'])
def get_movie(name):
    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    out = None
    if name not in datum.keys():
        return "404 Not Found"

    for each in datum.keys():
        if name == each:
            out = datum[each]
            break
    return jsonify(out)


# GET REQUESTS END HERE


@app.route("/actors/<name>", methods=['PUT'])
def put_actor(name):
    # if not request.json:
    #     abort(400)

    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    content = request.get_json()
    if name not in datum.keys():
        return "404 not found"
    lookup = datum[name]
    for each in content.keys():
        lookup[each] = content[each]
    datum[name] = lookup
    return "Status 201 updated"


@app.route("/movies/<name>", methods=['PUT'])
def put_movie(name):

    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    content = request.get_json()
    if name not in datum.keys():
        return "404 not found"
    lookup = datum[name]
    for each in content.keys():
        lookup[each] = content[each]
    datum[name] = lookup
    return "Status 201 updated"


# End of puts

@app.route("/actors", methods=['POST'])
def post_actor():
    if not request.json or 'name' not in request.json:
        abort(400)

    content = request.get_json()
    name = content["name"]
    datum[name] = content["name"]
    return "Status 201 updated"


@app.route("/movies", methods=['POST'])
def post_movie():
    # if not request.json or not 'name' not in request.json:
    #     abort(400)

    content = request.get_json()
    name = content["name"]
    datum[name] = content["name"]
    return "Status 201 updated"


# End of posts

@app.route("/actors/<name>", methods=['DELETE'])
def delete_actor(name):
    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    if name in datum.keys():
        del datum[name]
        return "Success 200"

    return "Failure 400"


@app.route("/movies/<name>", methods=['DELETE'])
def delete_movie(name):
    name = name.replace("'", "")
    name = name.replace("\"", "")
    name = name.replace("_", " ")
    if name in datum.keys():
        del datum[name]
        return "Success 200"

    return "Failure 400"

@app.route("/analysis/age_plot", methods=['GET'])
def age_trend():
    ages = []
    income = []
    for name in global_actors.keys():
        entry = None
        temp_dict = global_actors[name]
        if "age" in temp_dict.keys() and "total_gross" in temp_dict.keys():
            curr_age = temp_dict["age"]
            curr_gross = temp_dict["total_gross"]
            if curr_age > 0 and curr_gross > 0: # and curr_gross < 10000000:#(1000000000//10):
                if curr_gross < 10000:
                    curr_gross = curr_gross * 1000000
                ages.append(curr_age)
                income.append(curr_gross)

    z = np.polyfit(ages, income, 1)
    p = np.poly1d(z)
    plt.plot(ages, p(ages), "r--")

    plt.scatter(ages, income, alpha=0.5)
    plt.title('Plot of Ages and Grossing')
    plt.xlabel('Ages')
    plt.ylabel('Income')
    plt.savefig('age_plot.png', dpi=600)
    return "200 Successful"

@app.route("/analysis/age_group", methods=['GET'])
def get_groups():
    teens = []  # < 20
    young = []  # < 40
    middle = []  # < 60
    old = []  # < 80
    # "age": 61,
    # "total_gross": 562709189,
    for name in global_actors.keys():
        entry = None
        temp_dict = global_actors[name]
        if "age" in temp_dict.keys() and "total_gross" in temp_dict.keys():
            curr_age = temp_dict["age"]
            curr_gross = temp_dict["total_gross"]
            if curr_gross < 10000:
                curr_gross = curr_gross * 1000000
            if curr_age < 30:
                teens.append((name, curr_gross))
            elif 30 <= curr_age < 50:
                young.append((name, curr_gross))
            elif 50 <= curr_age < 70:
                middle.append((name, curr_gross))
            elif 70 <= curr_age < 90:
                old.append((name, curr_gross))

    totals = []
    total = 0
    curr_list = teens
    for entry in curr_list:
        total += entry[1]
    totals.append(total / len(curr_list))

    total = 0
    curr_list = young
    for entry in curr_list:
        total += entry[1]
    totals.append(total / len(curr_list))

    total = 0
    curr_list = middle
    for entry in curr_list:
        total += entry[1]
    totals.append(total / len(curr_list))

    total = 0
    curr_list = old
    for entry in curr_list:
        total += entry[1]
    totals.append(total / len(curr_list))

    for i in range(0, len(totals)):
        temp = totals[i]
        temp = math.floor(temp)
        totals[i] = temp



    objects = ["0-20", "20-40", "40-60", "60-80"]
    y_pos = np.arange(len(objects))
    connections = totals
    plt.figure(figsize=(10, 10))
    plt.bar(y_pos, connections, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Grossing (In tens of millions)')
    plt.xlabel('Age')
    plt.title('Grossing by Age Group')
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('age_groups.png', dpi=600)
    return "200 Successful"


@app.route("/analysis/hub", methods=['GET'])
def get_hub():
    hub_set = {}
    hub_list = []
    hub_counts = []
    # Loop below counts number of connections
    for name in datum.keys():
        entry = None
        actor_dict = datum[name]
        if actor_dict["json_class"] == "Actor":
            movies = actor_dict["movies"]
            count = 0
            for each in movies:
                if each in datum.keys():
                    movie_dict = datum[each]
                    if "actors" in movie_dict.keys():
                        count += len(movie_dict["actors"])
            hub_set[name] = count

    sorted_d = sorted(hub_set.items(), key=operator.itemgetter(1), reverse=True)

    # Gets the top ten actors
    for idx, value in enumerate(sorted_d):
        if idx > 10:
            break
        hub_list.append(value[0])
        hub_counts.append(value[1])

    objects = hub_list
    y_pos = np.arange(len(objects))
    connections = hub_counts
    print("here")
    plt.figure(figsize=(10, 10))
    plt.bar(y_pos, connections, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Connections')
    plt.title('Actors')
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig('hub.png', dpi=600)
    return "200 Successful"


if __name__ == '__main__':
    with open("./film_crawler/data.json", 'r') as json_file:
        temp = json.load(json_file)
        global_actors = temp[0]
        datum = temp[0]
        movies = temp[1]
        for each in movies.keys():
            payload = movies[each]
            datum[each] = payload

    app.run(debug=True)
