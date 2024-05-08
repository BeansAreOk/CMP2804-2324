class point:
    def __init__(self):         # Initialize instance variables with default values
        self.name = "node"

        self.coord = (0, 0, 0)
        self.orientation = (0, 0, 0, 0)

        self.edges = []         # Empty list to store edges

    def __init__(self, n):
        self.name = n["node"]["name"]                           # Extract the name from the dictionary

        xcoord = n["node"]["pose"]["position"]["x"]             # Extract coordinates from the dictionary
        ycoord = n["node"]["pose"]["position"]["y"]
        zcoord = n["node"]["pose"]["position"]["z"]
        self.coord = (xcoord, ycoord, zcoord)

        worientation = n["node"]["pose"]["orientation"]["w"]    # Extract orientation from the dictionary
        xorientation = n["node"]["pose"]["orientation"]["x"]
        yorientation = n["node"]["pose"]["orientation"]["y"]
        zorientation = n["node"]["pose"]["orientation"]["z"]
        self.orientation = (worientation, xorientation, yorientation, zorientation)

        self.edges = []                                         # Extract edges from the dictionary
        for edge in n["node"]["edges"]:
            self.edges.append(edge["node"])
  
    def __str__(self):
        return str(self.name) + str(self.coord) + str(self.orientation) + str(self.edges)           # Return string representation of the point object
    
    def yaml_point(self,map):
        try:
            edges = []
            for edge in self.edges:             # Adds each edge back to a Dictionary
                edge_yaml = {                   # Defines and builds the structure for the edges section of YAML file
                    "action": "move_base",
                    "edge_id": self.name + "_" + edge,
                    "node": edge
                    }
                edges.append(edge_yaml)
                
            yaml_data = {                       # Defines and builds the structure for the nodes section of YAML file
            "meta": {
                "map": map,
                "node": self.name},
            "node": {
                "name": self.name,
                "pose": {
                    "position": {"x": self.coord[0], "y": self.coord[1], "z": self.coord[2]},
                    "orientation": {"w": self.orientation[0], "x": self.orientation[1], "y": self.orientation[2], "z": self.orientation[3]}
                },
                "edges": edges
            }
            }
            return yaml_data
        except Exception as e:
            print(f"An error occurred while Fetching the YAML file: {e}")
            return False