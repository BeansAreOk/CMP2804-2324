import os.path
import yaml
from point import point

class map:
    

    def __init__(self):
        self.map_name = ""
        self.points = []

    def read_yaml(self, file_path):
        try:
            with open(file_path) as stream:
                values = yaml.safe_load(stream)
                yaml.nodes
                self.map_name = values["nodes"][0]["meta"]["map"] + ".png"
                print(values)

                for value in values["nodes"]:
                    node = point(value)
                    self.points.append(node)
                return True
        except:
            return False