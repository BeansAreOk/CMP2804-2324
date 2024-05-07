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