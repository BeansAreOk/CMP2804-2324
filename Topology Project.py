import PySimpleGUI as sg
import yaml
import os.path
from map import map

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
yaml_file = map()
map_scale = 10

def home():
    layout1 = [[sg.Text("Please choose an option:")], [sg.Button("Load YAML file")], [sg.Button("New YAML file")], [sg.Button("Exit")]]
    layout2 = [[sg.Text("Please enter the name of the YAML file you wish to open:", key="text1")], [sg.Input(key="INPUT")], [sg.Button("Ok", key="Ok1")], [sg.Button("Back", key="Back")]]
    layout3 = [[sg.Text("Please enter the name of the YAML file you wish to create:")], [sg.Input(key="INPUT2")], [sg.Button("Ok", key="Ok2")], [sg.Button("Back", key="Back2")]]
    layout4 = [[sg.Graph((800, 800), (-400, -400), (400, 400), background_color='white', key="GRAPH")]]
    layout =  [[sg.Column(layout1, key="COL1"), sg.Column(layout2, visible=False, key="COL2"), sg.Column(layout3, visible=False, key="COL3"), sg.Column(layout4, visible=False, key="COL4")]]
    window = sg.Window("Topology GUI", layout, margins=(250, 100))

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
        print("Map related to this YAML file not found")

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
        
    for point in yaml_file.points: # draw nodes
        xcoord = point.coord[0] * map_scale
        ycoord = point.coord[1] * map_scale
        window["GRAPH"].draw_point((xcoord, ycoord),size=8,color="blue")
        
    window["COL2"].update(visible=False)
    window["COL4"].update(visible=True)

    
home()