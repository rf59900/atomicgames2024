#!/usr/bin/python

import sys
import json
import random

if (sys.version_info > (3, 0)):
    print("Python 3.X detected")
    import socketserver as ss
else:
    print("Python 2.X detected")
    import SocketServer as ss


# class NetworkHandler(ss.StreamRequestHandler):
#     def handle(self):
#         game = Game()

#         while True:
#             data = self.rfile.readline().decode() # reads until '\n' encountered
#             json_data = json.loads(str(data))
#             # uncomment the following line to see pretty-printed data
#             print(json.dumps(json_data, indent=4, sort_keys=True))
#             response = game.get_random_move(json_data).encode()
#             self.wfile.write(response)

class NetworkHandler(ss.StreamRequestHandler):
    def handle(self):
        game = Game()
        
        count = 0
        while True:
            data = self.rfile.readline().decode()  # reads until '\n' encountered
            if not data.strip():  # skip empty lines
                continue

            try:
                json_data = json.loads(str(data))
            except Exception as e:
                print("Unexpected error:", e)

            if count == 0:
                game.initialize_map(json_data)

            response = game.get_random_move(json_data).encode()
            self.wfile.write(response)

            count += 1        

class Game:
    def __init__(self):
        self.units = set() # set of unique unit ids
        self.directions = ['N', 'S', 'E', 'W']


    def get_map_size(self, json_data):
        width = json_data["game_info"]["map_width"]
        height = json_data["game_info"]["map_height"]

        return (width, height)

    def initialize_map(self, json_data):
        map_dimensions = self.get_map_size(json_data)
        print("~~~~~~~~~~~~~~~~~~!!!!!!!!!!!!!!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~~~~")
        print(map_dimensions)
        two_dee_map = ([0] * map_dimensions[0])
        two_dee_map = [[0]*map_dimensions[0]]*map_dimensions[1]
        print(two_dee_map) # Print 2D Array

        return

    def get_random_move(self, json_data):
        #two_dee_map = self.initialize_map(json_data)
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter
        unit = random.choice(tuple(self.units))
        direction = 'E'
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit, "dir": direction}]}
        response = json.dumps(command, separators=(',',':')) + '\n'
        print(json_data["unit_updates"])
        #self.update_tiles(json_data, two_dee_map)

        return response

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
