import PySimpleGUI as sg
import yaml
import os.path
import numpy as np
from map import map
from point import point

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
yaml_file = map()
map_scale = 10
pointcoords = []
curr_point = 0
def home():
    want_to_move = False
    want_to_join = False
    want_to_unjoin = False
    menu = ["menu", ["New Node", 'Move Node', "Join Nodes", "Unjoin Nodes", "Delete Node"]]
    layout1 = [[sg.Text("Please choose an option:")], [sg.Button("Load YAML file")], [sg.Button("New YAML file")], [sg.Button("Exit")]]
    layout2 = [[sg.Text("Please enter the name of the YAML file you wish to open:", key="text1")], [sg.Input(key="INPUT")], [sg.Button("Ok", key="Ok1")], [sg.Button("Back", key="Back")]]
    layout3 = [[sg.Text("Please enter the name of the YAML file you wish to create:")], [sg.Input(key="INPUT2")], [sg.Button("Ok", key="Ok2")], [sg.Button("Back", key="Back2")]]
    layout4 = [[sg.Graph((800, 800), (-400, -400), (400, 400), background_color='white',enable_events = True,right_click_menu = menu, key="GRAPH")]]
    layout5 = [[sg.Text("To add, move, join and delete nodes please right click on the display area to the left.")],[sg.Text("When moving a node the selected node will be displayed in red and when joining it will be green.")],[sg.Text("When moving a node left click where you wish to move it to after selecting your node.")],[sg.Button("Save", key ="save")],[sg.Button("Back", key ="Back4")]]
    layout =  [[sg.Column(layout1, key="COL1"), sg.Column(layout2, visible=False, key="COL2"), sg.Column(layout3, visible=False, key="COL3"), sg.Column(layout4, visible=False, key="COL4"), sg.Column(layout5, visible=False, key="COL5")]]
    window = sg.Window("Topology GUI", layout, resizable=True).Finalize()
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == "Load YAML file":
            window["COL1"].update(visible=False)
            window["COL2"].update(visible=True)
        elif event == "New YAML file":
            window["COL1"].update(visible=False)
            window["COL3"].update(visible=True)
        elif event == "Ok1":
            file1 = values["INPUT"] 
            if load_yaml(file1):
                draw_map(window)
            else:
                window["text1"].update(["File not found."])
        elif event == "Ok2":
            file1 = values["INPUT2"] 
            new_yaml(file1)
            draw_map(window)
        elif event == "Back":
            window["COL2"].update(visible=False)
            window["COL1"].update(visible=True)
        elif event == "Back2":
            window["COL3"].update(visible=False)
            window["COL1"].update(visible=True)
        elif event == "Back4":
            window["COL4"].update(visible=False)
            window["COL5"].update(visible=False)
            window["COL1"].update(visible=True)
            window.normal()
            yaml_file.map_name = ""
            yaml_file.points = []
        elif event == "save":
            sg.Popup()
        elif event in ("New Node"):
            want_to_move = False
            want_to_join = False
            want_to_unjoin = False
            x, y = values["GRAPH"]
            node_name = sg.popup_get_text("Please enter a name for the node")
            add_point(node_name, x, y)
            draw_map(window)
        elif event in ("Move Node"):
            want_to_move = False
            want_to_join = False
            want_to_unjoin = False
            x, y = values["GRAPH"]
            curr_point = nearest_point([x,y],pointcoords)
            window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="red")
            want_to_move = True
        elif event in ("GRAPH"):
            x, y = values["GRAPH"]
            if want_to_move == True:
                move_point(curr_point,[x/10,y/10,0])
                draw_map(window)
            elif want_to_join == True:
                join_points(curr_point, nearest_point([x,y],pointcoords))
                draw_map(window)
            elif want_to_unjoin == True:
                unjoin_points(curr_point, nearest_point([x,y],pointcoords))
                draw_map(window)
        elif event in ("Join Nodes"):
            want_to_move = False
            want_to_join = False
            want_to_unjoin = False
            x, y = values["GRAPH"]
            curr_point = nearest_point([x,y],pointcoords)
            window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="green")
            want_to_join = True
        elif event in ("Unjoin Nodes"):
            want_to_move = False
            want_to_join = False
            want_to_unjoin = False
            x, y = values["GRAPH"]
            curr_point = nearest_point([x,y],pointcoords)
            window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="green")
            want_to_unjoin = True
        elif event in ("Delete Node"):
            want_to_move = False
            want_to_join = False
            want_to_unjoin = False
            x, y = values["GRAPH"]
            del_point(nearest_point([x,y],pointcoords))
            draw_map(window)
    window.close()

def load_yaml(filename):
    if not filename.endswith(".yml"):
            filename = filename + ".yml"

    return yaml_file.read(os.path.join(__location__, filename))

def save_yaml(filename, original_filename = "default.yml"):
    if not filename.endswith(".yml"):
            filename = filename + ".yml"

    return yaml_file.write(os.path.join(__location__, filename), os.path.join(__location__, original_filename))

def new_yaml(name):
    yaml_file.new(name)

def draw_map(window):
    try:
        window["GRAPH"].draw_image(os.path.join(__location__, yaml_file.map_name + ".png"), location=(-400,400))
    except:
        sg.Popup("Map related to this YAML file not found, using blank map.")

    for point in yaml_file.points: # draw edges
        xcoord = point.coord[0] * map_scale
        ycoord = point.coord[1] * map_scale
        xcoord2 = xcoord
        ycoord2 = ycoord

        for edge in point.edges:
            for point2 in yaml_file.points:
                if point2.name == edge:
                    xcoord2 = point2.coord[0] * map_scale
                    ycoord2 = point2.coord[1] * map_scale
            if xcoord != xcoord2 or ycoord != ycoord2:
                window["GRAPH"].draw_line((xcoord, ycoord), (xcoord2, ycoord2))
    pointcoords.clear()   
    for point in yaml_file.points: # draw nodes
        xcoord = point.coord[0] * map_scale
        ycoord = point.coord[1] * map_scale
        
        pointcoords.append([xcoord, ycoord])
        window["GRAPH"].draw_point((xcoord, ycoord),size=8,color="blue")
        
    window["COL2"].update(visible=False)
    window["COL3"].update(visible=False)
    window["COL4"].update(visible=True)
    window["COL5"].update(visible=True)
    window.Maximize()

def add_point(name,x, y):
    yaml_data = {
        "node": {
            "name": name,
            "pose": {
                "position": {"x": int(x/10), "y": int(y/10), "z": 0.0},
                "orientation": {"w": 0, "x": 0, "y": 0, "z": 0}
            },
            "edges": []
        }
    }
    value = point(yaml_data)
    yaml_file.points.append(value)
    
def nearest_point(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return np.argmin(dist_2)

def del_point(index):
    yaml_file.points.pop(index)

def move_point(index,coords):
    yaml_file.points[index].coord = coords
    
def join_points(point1, point2):
    if yaml_file.points[point2].name not in yaml_file.points[point1].edges:
        yaml_file.points[point1].edges.append(yaml_file.points[point2].name)
    if yaml_file.points[point1].name not in yaml_file.points[point2].edges:    
        yaml_file.points[point2].edges.append(yaml_file.points[point1].name)
def unjoin_points(point1, point2):
    if yaml_file.points[point2].name in yaml_file.points[point1].edges:
        yaml_file.points[point1].edges.remove(yaml_file.points[point2].name)
    if yaml_file.points[point1].name in yaml_file.points[point2].edges:    
        yaml_file.points[point2].edges.remove(yaml_file.points[point1].name)
home()