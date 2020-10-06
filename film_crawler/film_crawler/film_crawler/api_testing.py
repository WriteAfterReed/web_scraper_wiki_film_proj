import requests
import json

def test_get():
    print("")
    print("Test 1st get")
    r = requests.get("http://127.0.0.1:5000/actors/Bruce_Willis")
    print(r.json())

    print("")
    print("Test 2nd get")
    r = requests.get("http://127.0.0.1:5000/movies/Die_Hard_2")
    print(r.json())


    print("")
    print("Test 3rd get")
    r = requests.get("http://127.0.0.1:5000/actors?name='Bob'")
    print(r.json())

    print("")
    print("Test 4th get")
    r = requests.get("http://127.0.0.1:5000/movies?name='Die'")
    print(r.json())


    print("")
    print("Test 5th get")
    r = requests.get("http://127.0.0.1:5000/movies?name='Die'|'Hard'")
    print(r.json())


    print("")
    print("Test 6th get")
    r = requests.get("http://127.0.0.1:5000/movies?name='Bruce'&'Willis'")
    print(r.json())


def test_put():
    print("")
    print("Test 1 put")
    r = requests.put('http://127.0.0.1:5000/actors/Bruce_Willis', json={"total_gross": 500})
    print(r.text)
    r = requests.get("http://127.0.0.1:5000/actors/Bruce_Willis")
    print(r.json())

    print("")
    print("Test 2 put")
    r = requests.put('http://127.0.0.1:5000/movies/Die_Hard', json={"box_office": 500})
    print(r.text)

    r = requests.get("http://127.0.0.1:5000/movies/Die_Hard")
    print(r.json())


def test_post():
    print("")
    print("Test 1 post")
    r = requests.post("http://127.0.0.1:5000/actors", json={"name": "Billy Joe"})
    print(r.text)

    r = requests.get("http://127.0.0.1:5000/actors/Billy_Joe")
    print(r.json())

    print("")
    print("Test 2 post")
    r = requests.post("http://127.0.0.1:5000/movies", json={"name": "Captain America"})
    print(r.text)

    r = requests.get("http://127.0.0.1:5000/movies/Captain_America")
    print(r.json())

def test_delete():

    print("")
    print("Test 1 DEL")
    r = requests.delete("http://127.0.0.1:5000/actors/Bruce_Willis")

    r = requests.get("http://127.0.0.1:5000/actors/Bruce_Willis")
    print(r.text)

    print("")
    print("Test 2 DEL")
    r = requests.delete("http://127.0.0.1:5000/movies/Die_Hard")
    r = requests.get("http://127.0.0.1:5000/movies/Die_Hard")
    print(r.text)


def test_analysis():
    print("")
    print("Test Generate Analysis")
    r = requests.get("http://127.0.0.1:5000/analysis/age_plot")

    r = requests.get("http://127.0.0.1:5000/analysis/age_group")

    r = requests.get("http://127.0.0.1:5000/analysis/hub")


if __name__ == "__main__":
    print("Start Tests")
    test_get()
    test_put()
    test_post()
    test_delete()
    test_analysis()
    print("End Tests")
