import json

from flask import request


def dump_data(player_list):
  
    with open("gamefiles/players.json", mode="w", encoding="utf-8") as json_data:
        json.dump(player_list, json_data)
        
def get_json_data():
   
    with open("gamefiles/players.json", "r") as json_file:
        json_data = json.load(json_file)
        return json_data



def create_riddle_data(number_of_players):
   
    player_list = []
    for i in range(number_of_players):
        username = request.form["player-{0}-username".format(i + 1)]
        player_object = {
            "username": username,
            "lives": 3,
            "score": 0,
            "question": "",
            "last question correct": True,  
            "turn": False, 
            "previous": False,
            "answer": "",
            "no": i + 1,
            "incorrect guesses": ""
        }
        player_list.append(player_object)
    dump_data(player_list)