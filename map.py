import os.path
import yaml
from point import point

class map:
    map_name = ""
    points = []

    def __init__(self) -> None:
        pass

    def read_yaml(self, file_path):
        try:
            with open(file_path) as stream:
                values = yaml.safe_load(stream)
                yaml.nodes
                self.map_name = values[0]["meta"]["map"] + ".png"
                print(values)
                for value in values:
                    xcoord = value["node"]["pose"]["position"]["x"]
                    ycoord = value["node"]["pose"]["position"]["y"]
                    self.points.append(point((xcoord, ycoord)))
                return True
        except:
            return False