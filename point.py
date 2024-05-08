class point:
    def __init__(self):
        self.name = "node"

        self.coord = (0, 0, 0)
        self.orientation = (0, 0, 0, 0)

        self.edges = []

    def __init__(self, n):
        self.name = n["node"]["name"]

        xcoord = n["node"]["pose"]["position"]["x"]
        ycoord = n["node"]["pose"]["position"]["y"]
        zcoord = n["node"]["pose"]["position"]["z"]
        self.coord = (xcoord, ycoord, zcoord)

        worientation = n["node"]["pose"]["orientation"]["w"]
        xorientation = n["node"]["pose"]["orientation"]["x"]
        yorientation = n["node"]["pose"]["orientation"]["y"]
        zorientation = n["node"]["pose"]["orientation"]["z"]
        self.orientation = (worientation, xorientation, yorientation, zorientation)

        self.edges = []
        for edge in n["node"]["edges"]:
            self.edges.append(edge["node"])
  
    def __str__(self):
        return str(self.name) + str(self.coord) + str(self.orientation) + str(self.edges)
    
    def yaml_point(self,map):
        edges = []
        for edge in self.edges:
            edge_yaml = {
                "action": "move_base",
                "edge_id": self.name + "_" + edge,
                "node": edge
                }
            edges.append(edge_yaml)
        yaml_data = {  
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