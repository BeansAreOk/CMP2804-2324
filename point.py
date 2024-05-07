class point:
    
    def __init__(self, n):
        self.name = n["node"]["name"]

        xcoord = n["node"]["pose"]["position"]["x"]
        ycoord = n["node"]["pose"]["position"]["y"]
        zcoord = n["node"]["pose"]["position"]["z"]
        self.coord = (xcoord, ycoord, zcoord)

        self.edges = []
        for edge in n["node"]["edges"]:
            self.edges.append(edge["node"])

