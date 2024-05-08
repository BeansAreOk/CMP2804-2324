import yaml                 # Importing the yaml module for YAML file handling
from point import point     # Importing the point class, presumably used for managing map points

class map:
    def __init__(self):
        self.map_name = ""  # Initializing map_name attribute to an empty string
        self.points = []    # Initializing points attribute to an empty list

    def __str__(self):
        return str(self.map_name) + str(self.points)    # Returning a string representation of map_name and points
    
    def new(self, name):
        self.map_name = name    # Setting the map_name attribute to the provided name
        self.points.clear()     # Clearing the list of points

    def read(self, file_path):
        try:
            with open(file_path, 'r') as stream:    # Opening the file specified by file_path in read mode
                values = yaml.safe_load(stream)     # Loading YAML data from the file into values
                yaml.nodes
                
                if values is None:
                    return False        # Return False if YAML data is empty or None
                
                self.map_name = values["name"]      # Setting map_name to the "name" field from the YAML data

                self.points.clear()     # Clearing the list of points
                
                if "nodes" in values:               # Looping through the "nodes" field in the YAML data
                    for value in values["nodes"]:   # Creating a new point object from the data
                        node = point(value)         # Appending the point object to the list of points
                        self.points.append(node)    # Returning True to indicate successful reading
                
                return True             # Returning True to indicate successful reading
            
        except Exception as e:
            print(f"An error occurred while reading the YAML file: {e}")
            return False                # Returning False if an exception occurs during reading
    
    # Function to write map data to a YAML file   
    def write(self): 
        try:
            nodedata = []
            for point in self.points:       #Puts all the nodes in the points array into a dictionary in YAML format
                nodedata.append(point.yaml_point(self.map_name))
            data = {                        #Defines the main body of the YAML file for saving
                "name" : self.map_name,
                "metric_map" : "",
                "meta" : {"last_updated": "2021-04-21_08-23-39"},
                "metric_map" : self.map_name,
                
                "nodes" : nodedata
                }
            return data
        except Exception as e:
            print(f"An error occurred while fetching the YAML file: {e}")
            return False