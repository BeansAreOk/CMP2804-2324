import os.path
import yaml
from point import point

class map:
    def __init__(self):
        self.map_name = ""
        self.points = []

    def __str__(self):
        return str(self.map_name) + str(self.points)
    
    def new(self, name):
        self.map_name = name
        self.points.clear()

    def read(self, file_path):
        try:
            with open(file_path, 'r') as stream:
                values = yaml.safe_load(stream)
                yaml.nodes
                self.map_name = values["name"]
                #print(values)

                self.points.clear()
                for value in values["nodes"]:
                    node = point(value)
                    self.points.append(node)
                return True
        except:
            return False
        
    def write(self): 
        nodedata = []
        for point in self.points:
            nodedata.append(point.yaml_point(self.map_name))
        data = {
            "name" : self.map_name,
            "metric_map" : "",
            "meta" : {"last_updated": "2021-04-21_08-23-39"},
            "metric_map" : self.map_name,
            
            "nodes" : nodedata
            }
        return data