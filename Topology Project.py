import PySimpleGUI as sg
import yaml
import os.path
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
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
            file = os.path.join(__location__, file1)
            try:
                with open(file) as stream:
                    values = yaml.safe_load(stream)
                    map = os.path.join(__location__, values[0]["meta"]["map"] + ".png")
                    print(values)
                    try:
                        window["GRAPH"].draw_image(map, location=(-400,400))
                        pointval = 0
                        for value in values:
                            print(pointval)
                            xcoord = value["node"]["pose"]["position"]["x"]*100
                            ycoord = value["node"]["pose"]["position"]["y"]*100
                            if pointval == 0:
                                coords = (xcoord,ycoord)
                                pointval = pointval +1
                            elif pointval == 1:
                                coords2 = (xcoord,ycoord)
                                window["GRAPH"].draw_line(coords, coords2)
                                coords = coords2
                            window["GRAPH"].draw_point((xcoord, ycoord),size=8,color="blue")
                        window["COL2"].update(visible=False)
                        window["COL4"].update(visible=True)
                    except:
                        window["text1"].update(["Map related to this YAML file not found"])
            except:
                window["text1"].update(["File not found."])
        elif event == "Ok2":
            file1 = values["INPUT2"] 
            print(file1)
        elif event == "Back":
            window["COL2"].update(visible=False)
            window["COL1"].update(visible=True)
        elif event == "Back2":
            window["COL3"].update(visible=False)
            window["COL1"].update(visible=True)

    window.close()
    
home()