import PySimpleGUI as sg
import yaml
import os.path
import numpy as np
from map import map
from point import point

# Get the current directory
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Define the main function for GUI operation
yaml_file = map()
map_scale = 10
pointcoords = []
curr_point = 0
has_image = True
def home():
    try:
        want_to_move = False
        want_to_join = False
        want_to_unjoin = False
        file1 = ""
        # Define GUI layouts
        menu = ["menu", ["New Node", "Move Node", "Join Nodes", "Unjoin Nodes", "Edit Node", "Delete Node"]]
        layout1 = [[sg.Text("Please choose an option:")], [sg.Button("Load YAML file")], [sg.Button("New YAML file")], [sg.Button("Exit")]]
        layout2 = [[sg.Text("Please enter the name of the YAML file you wish to open:", key="text1")], [sg.Input(key="INPUT")], [sg.Button("Ok", key="Ok1")], [sg.Button("Back", key="Back")]]
        layout3 = [[sg.Text("Please enter the name of the YAML file you wish to create:", key="text2")], [sg.Input(key="INPUT2")], [sg.Button("Ok", key="Ok2")], [sg.Button("Back", key="Back2")]]
        layout4 = [[sg.Graph((800, 800), (-400, -400), (400, 400), background_color='white',enable_events = True,right_click_menu = menu, key="GRAPH")]]
        layout5 = [[sg.Text("To add, move, join and delete nodes please right click on the display area to the left.")],[sg.Text("When moving a node the selected node will be displayed in red and when joining it will be green.")],[sg.Text("When moving a node left click where you wish to move it to after selecting your node.")],[sg.Text("If you wish to view/edit information relating to nodes right click on them and select Edit Node.")],[sg.Button("Save", key ="save")],[sg.Button("Back", key ="Back4")]]
        layout =  [[sg.Column(layout1, key="COL1"), sg.Column(layout2, visible=False, key="COL2"), sg.Column(layout3, visible=False, key="COL3"), sg.Column(layout4, visible=False, key="COL4"), sg.Column(layout5, visible=False, key="COL5")]]
        
        # Create the GUI window
        window = sg.Window("Topology GUI", layout, resizable=True).Finalize()
        
        # Event loop to handle GUI events
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:   #Closes window
                break
            elif event == "Load YAML file":
                window["COL1"].update(visible=False)    #Switches visibility of windows
                window["COL2"].update(visible=True)
            elif event == "New YAML file":
                window["COL1"].update(visible=False)    #Switches visibility of windows
                window["COL3"].update(visible=True)
            elif event == "Ok1":
                file1 = values["INPUT"] 
                if load_yaml(file_type(file1)):         #Tries to load the YAML file and draw the data                  
                    draw_map(window)
                else:
                    window["text1"].update("File not found.")
            elif event == "Ok2":
                file1 = values["INPUT2"] 
                if os.path.isfile(os.path.join(__location__,(file_type(file1)))):   #Checks file doesnt exist already and name isnt blank before trying to create new YAML file and draw
                    window["text2"].update("File already exists")
                elif file1 != "":
                    new_yaml(file1)
                    draw_map(window)
                else:
                    window["text2"].update("Please enter a file name.")
            elif event == "Back":
                window["COL2"].update(visible=False)    #Switches visibility of windows
                window["COL1"].update(visible=True)
            elif event == "Back2":
                window["COL3"].update(visible=False)    #Switches visibility of windows
                window["COL1"].update(visible=True)
            elif event == "Back4":
                window["COL4"].update(visible=False)    #Switches visibility of windows
                window["COL5"].update(visible=False)
                window["COL1"].update(visible=True)
                window.normal()                         #Shrinks the window out of full screen and erases the data on the graph
                window["GRAPH"].erase()
                global has_image
                has_image = True
            elif event == "save":
                sg.Popup("File Saved")                  #Saves the File
                save_file(file1)
            elif event in ("New Node"):                 #Right click function disables all active functions
                want_to_move = False
                want_to_join = False
                want_to_unjoin = False
                x, y = values["GRAPH"]
                while True:
                    node_name = sg.popup_get_text("Please enter a name for the node")
                    if node_name != "":
                        add_point(node_name, x, y)
                        draw_map(window)
                        break
            elif event in ("Move Node"):
                want_to_move = False                    #Right click function disables all active functions
                want_to_join = False
                want_to_unjoin = False
                x, y = values["GRAPH"]                  #Gets current mouse coordinates and locates nearest point to them
                curr_point = nearest_point([x,y],pointcoords)
                window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="red")        #recoloours point to red for easier visibility
                want_to_move = True                                                             #sets the point as wanting to move so it will on click
            elif event in ("Join Nodes"):
                want_to_move = False                #Right click function disables all active functions
                want_to_join = False
                want_to_unjoin = False
                x, y = values["GRAPH"]              #Gets current mouse coordinates and locates nearest point to them
                curr_point = nearest_point([x,y],pointcoords)
                window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="green")      #recoloours point to green for easier visibility
                want_to_join = True                                                             #sets the point as wanting to create an edge so it will on click
            elif event in ("Unjoin Nodes"):
                want_to_move = False                #Right click function disables all active functions
                want_to_join = False
                want_to_unjoin = False
                x, y = values["GRAPH"]              #Gets current mouse coordinates and locates nearest point to them
                curr_point = nearest_point([x,y],pointcoords)
                window["GRAPH"].draw_point((pointcoords[curr_point]),size=8,color="green")      #recoloours point to red for easier visibility
                want_to_unjoin = True                                                           #sets the point as wanting to destroy an edge so it will on click
            elif event in ("Edit Node"):
                want_to_move = False                #Right click function disables all active functions
                want_to_join = False    
                want_to_unjoin = False
                x, y = values["GRAPH"]              #Gets current mouse coordinates and locates nearest point to them
                curr_point = nearest_point([x,y],pointcoords)
                edit_window(curr_point, window)     #Opens the seperate edit window allowing you to view information about a point and change some of it
            elif event in ("Delete Node"):
                want_to_move = False                #Right click function disables all active functions
                want_to_join = False    
                want_to_unjoin = False
                x, y = values["GRAPH"]              #Gets current mouse coordinates and locates nearest point to them
                del_point(nearest_point([x,y],pointcoords))     #Deletes node and then redraws graph
                draw_map(window)
            elif event in ("GRAPH"):
                x, y = values["GRAPH"]              #Gets current mouse coordinates from click
                if want_to_move == True:
                    move_point(curr_point,[x/map_scale,y/map_scale,0])    #If want to move is true it moves old point to new location
                    draw_map(window)
                elif want_to_join == True:
                    join_points(curr_point, nearest_point([x,y],pointcoords))   #If want to join is true it creates an edge between old point and point closest to new click
                    draw_map(window)
                elif want_to_unjoin == True:            
                    unjoin_points(curr_point, nearest_point([x,y],pointcoords)) #If want to unjoin is true it destroys an edge between old point and point closest to new click
                    draw_map(window)    
        window.close()
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# checks that the file is of the right type
def file_type(filename):
    if not filename.endswith(".yml"):
        filename = filename + ".yml"
    return filename

# load YAML file and saves it data to yaml_file
def load_yaml(filename):
    try:    
        return yaml_file.read(os.path.join(__location__, filename))
    except Exception as e:
        sg.popup_error(f"An error occurred while loading the YAML file: {e}")
        return False

# Function to create a new YAML file
def new_yaml(name):
    try:
        yaml_file.new(name)
    except Exception as e:
        sg.popup_error(f"An error occurred while creating a new YAML file: {e}")
        
#Function to add the background map to the GUI 
def add_image(window):
    global has_image
    if has_image == True:
        try:
            window["GRAPH"].draw_image(os.path.join(__location__, yaml_file.map_name + ".png"), location=(-400,400))        #Tries to draw the map image under the graph if its available
        except Exception:
            has_image = False
            sg.popup("Map related to this YAML file:",yaml_file.map_name,"Not found, using blank map.")
            
# Function to draw the nodes and edges on the GUI window
def draw_map(window):
    
    window["GRAPH"].erase() # clear old map for a redraw
    add_image(window)
    
    # Draw edges
    for point in yaml_file.points:                  #Goes through every node temporarily saving their coordinates
        xcoord = point.coord[0] * map_scale
        ycoord = point.coord[1] * map_scale
        xcoord2 = xcoord
        ycoord2 = ycoord

        for edge in point.edges:                    #Goes through every edge in each node
            for point2 in yaml_file.points:         #Runs through every node again in order to compare their name to the edges of the other node
                if point2.name == edge:
                    xcoord2 = point2.coord[0] * map_scale
                    ycoord2 = point2.coord[1] * map_scale
            if xcoord != xcoord2 or ycoord != ycoord2:                              #If they have edges they are then drawn
                window["GRAPH"].draw_line((xcoord, ycoord), (xcoord2, ycoord2))
                
    # Draw nodes
    pointcoords.clear()                         #clears pointcoords to avoid repeated node
    for point in yaml_file.points:              #Goes through every node appending them to pointcoords and drawing them on the graph
        xcoord = point.coord[0] * map_scale
        ycoord = point.coord[1] * map_scale   
        pointcoords.append([xcoord, ycoord])
        window["GRAPH"].draw_point((xcoord, ycoord),size=8,color="blue")
    window["COL2"].update(visible=False)                #Switches visibility of windows
    window["COL3"].update(visible=False)
    window["COL4"].update(visible=True)
    window["COL5"].update(visible=True)
    window.Maximize()                                   #Fullscreens the window for better visibility

#Function to find the largest point (not currently used, possibly for changing scale of the graph in future)
def largest_point():
    far_coord = []
    big_coord = 0
    try:
        for point in pointcoords:
            point = np.asarray(point)                               #places the point in a numpy array
            far_coord.append(point[(np.abs(point - 0)).argmax()])   #appends x or y to far_coord array depending on which is further from 0
        far_coord = np.asarray(far_coord)                           #turns far_coord into a numpy array
        big_coord = (far_coord[(np.abs(far_coord - 0)).argmax()])   #Finds the value furthest from 0 and sets it as the variable big_coord
        return big_coord
    except Exception as e:
        sg.popup_error(f"An error occurred while finding largest node: {e}")
# Function to add a new node
def add_point(name,x, y):
    try:
        yaml_data = {                       #creates the information for a new point in the correct format to be fed into the point class as a new object
            "node": {
                "name": name,
                "pose": {
                    "position": {"x": int(x/map_scale), "y": int(y/map_scale), "z": 0.0},
                    "orientation": {"w": 0, "x": 0, "y": 0, "z": 0}
                },
                "edges": []
            }   
        }
        value = point(yaml_data)
        yaml_file.points.append(value)      #puts the new object into the yaml_file objects points array
    except Exception as e:
        sg.popup_error(f"An error occurred while adding a new node: {e}")

# Function to find the nearest point to a given coordinate
def nearest_point(node, nodes):
    try:
        nodes = np.asarray(nodes)
        dist_2 = np.sum((nodes - node)**2, axis=1)      #This takes some coords and the list of all nodes and first finds the vector difference to each node then squares it to find the euclidian distance then sums them on the axis 1
        return np.argmin(dist_2)                        #This then finds the node with the smallest distance and returns it
    except Exception as e:
        sg.popup_error(f"An error occurred while finding the nearest point: {e}")
        return None

# Function to delete a node
def del_point(index):
    try:
        yaml_file.points.pop(index)
    except Exception as e:
        sg.popup_error(f"An error occurred while deleting the node: {e}")

# Function to move a node
def move_point(index,coords):
    try:
        yaml_file.points[index].coord = coords
    except Exception as e:
        sg.popup_error(f"An error occurred while moving the node: {e}")

# Function to join two nodes   
def join_points(point1, point2):
    try:
        if yaml_file.points[point2].name not in yaml_file.points[point1].edges:         #checks if they are already joined and if not joins them
            yaml_file.points[point1].edges.append(yaml_file.points[point2].name)
        if yaml_file.points[point1].name not in yaml_file.points[point2].edges:         #checks if they are already joined and if not joins them
            yaml_file.points[point2].edges.append(yaml_file.points[point1].name)        
    except Exception as e:
        sg.popup_error(f"An error occurred while joining nodes: {e}")
 
# Function to unjoin two nodes       
def unjoin_points(point1, point2):
    try:
        if yaml_file.points[point2].name in yaml_file.points[point1].edges:             #checks if they are already joined and if they are removes the edge
            yaml_file.points[point1].edges.remove(yaml_file.points[point2].name)
        if yaml_file.points[point1].name in yaml_file.points[point2].edges:             #checks if they are already joined and if they are removes the edge
            yaml_file.points[point2].edges.remove(yaml_file.points[point1].name)
    except Exception as e:
        sg.popup_error(f"An error occurred while unjoining nodes: {e}")
  
# save YAML data to the specified filename
def save_file(filename):
    try:
        data = yaml_file.write()
        filename = file_type(os.path.join(__location__,filename))
        with open(filename, 'w') as stream:     # Opening the specified file path in write mode
            yaml.dump(data, stream)             # Writing updated YAML data to the file
    except Exception as e:
            sg.popup_error(f"An error occurred while writing the YAML file: {e}")
    
# Seperate window to display the information of a point and edit some of it
def edit_window(point,window):
    try:
        # Define the layout of the window
        layout = [[sg.Text("Node name")],[sg.InputText(yaml_file.points[point].name, key="name")],[sg.Text("Node Coordinates (Please make sure they are whole numbers in the same format and within the range of (-400, 400))")],[sg.InputText(("(",yaml_file.points[point].coord[0] * map_scale,"," ,yaml_file.points[point].coord[1] * map_scale,")"), key="coord")],[sg.Text("Node Edges (If you wish to edit edges please use the tool within the gui)")],[sg.InputText(yaml_file.points[point].edges, key="edges")],[sg.Button("Update", key="update")],[sg.Button("Close", key="Exit")]]
        
        # Create the GUI window
        window2 = sg.Window("test", layout)
        
        # Event loop to handle GUI events
        while True:
            event, values = window2.read()
            if event == "Exit" or event == sg.WIN_CLOSED:       #Closes window
                break
            elif event == "update":                             #Updates the value of a nodes name and coordinated when update button pressed
                newname = values["name"]
                yaml_file.points[point].name = newname          #Updates name attribute
                val = values["coord"]
                newcoord = val.replace("(", "").replace(")", "").replace(".0", "").split((", " or " "))     #formats the coords so they are accepted
                if is_int(newcoord[0]) and is_int(newcoord[1]):                                             #checks the values are integers and they are within correct range
                    if (-400 <= int(newcoord[0]) <= 400) and (-400 <= int(newcoord[1]) <= 400):
                        yaml_file.points[point].coord = [int(newcoord[0])/map_scale,int(newcoord[1])/map_scale,0]       #Updates coord attributes
                draw_map(window)                                #redraws graph so update visible
        window2.close()  
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")
        
# Function to check if a value is an integer before assuming it is            
def is_int(val):  
    try: 
        int(val)
    except ValueError:
        return False
    else:
        return True
    
home()