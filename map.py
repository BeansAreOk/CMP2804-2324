import yaml  
from point import point 

class map:

    # Initializes attributes to empty string/list
    def __init__(self):
        self.map_name = ""  
        self.points = [] 

    def __str__(self):
        return str(self.map_name) + str(self.points)
    
    # Creates a new map
    def new(self, name):
        self.map_name = name
        self.points.clear() # makes the points list empty

    # Reads and processes map data from yaml file
    def read(self, file_path):
        try:
            with open(file_path, 'r') as stream: #opens the file in read only mode
                values = yaml.safe_load(stream) #loads the data from the yaml file into the values variable
                yaml.nodes
                
                if values is None:
                    return False  
                
                self.map_name = values["name"]

                self.points.clear() #makes the points list empty 
                
                if "nodes" in values:    
                    for value in values["nodes"]: #Iterates over each item in the list that is linked with "nodes"
                        node = point(value) #creates a point object with value as an argument and calls it a node
                        self.points.append(node) #appends the node object to the points list                
                return True           
            
        except Exception as e:
            print(f"An error occurred while reading the YAML file: {e}")
            return False                
    
    # Returns the data in yaml format 
    def write(self): 
        try:
            nodedata = [] #inititializes an empty list called nodedata
            for point in self.points: #for loop that iterates over each element in the self.points list
                nodedata.append(point.yaml_point(self.map_name)) #calls yaml_point method for all point objects and appends the result to the nodedata list
            #initiliazes a dictionary called data with multiple key value pairs
            data = {     
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