import os.path
import yaml
from point import point

class map:
    def __init__(self):
        self.map_name = ""
        self.points = []

    def new(self, name):
        self.map_name = name
        self.points.clear()

    def read(self, file_path):
        try:
            with open(file_path, 'r') as stream:
                values = yaml.safe_load(stream)
                yaml.nodes
                self.map_name = values["name"]
                print(values)

                self.points.clear()
                for value in values["nodes"]:
                    node = point(value)
                    self.points.append(node)
                return True
        except:
            return False
        
    def write(self, file_path, original_path):
        '''
        data = {
            "name" : self.map_name,
            "metric_map" : ,
            "meta" : {"last_updated": "2021-04-21_08-23-39"},
            "metric_map" : self.map_name,
            
            "nodes" : [{
                "meta": {
                    "map": self.map_name, 
                    "node" : node.name,
                    "pointset" : self.map_name
                }, 
                "node": {
                    "edges": [{
                        "action" : "action",
                        "action" : "action",
                        "action" : "action",
                        "action" : "action",
                        "action" : "action",
                        "action" : "action",
                    }]
                }   
            }]
        }
        '''
        with open(os.path.join(original_path), 'r') as stream:
            values = yaml.safe_load(stream)

            values["name"] = self.map_name

            with open(file_path, 'w') as stream:
                yaml.dump(values, stream, default_flow_style=False, sort_keys=False)