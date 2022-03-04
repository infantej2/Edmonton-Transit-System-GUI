TITLE = "Cmpt103W21_X04L_ETS_JI.py 1.00 2021/04/07 INFANTE JETHRO"

'''
Edmonton Transist System Project

From lab specs: This program parses Edmonton Transit System (ETS) data
available from the City of Edmonton Open Data Catalogue and provides a user
interface to explore some of these data. 

Author: Jethro Infante
'''

from pprint import PrettyPrinter, pprint
def pp(X, w=50): PrettyPrinter(indent=2, width=w).pprint(X)
import pickle
from graphics import *

#==============================================================================
# Constants
menustr = '''
    Edmonton Transit System
---------------------------------
(1) Load shape IDs from GTFS file
(2) Load shapes from GTFS file
(3) Load stops from GTFS file

(4) Print shape IDs for a route
(5) Print points for a shape ID
(6) Print Stops for a location

(7) Save shapes, shape IDs, and stops in a pickle
(8) Load shapes, shape IDs, and stops from a pickle

(9) Display interactive map

(0) Quit
'''
giFname = "Background.gif"
LONG_L, LAT_L, LONG_R, LAT_U = -113.7136, 53.39576, -113.2714, 53.71605

#=============================================================================
'''
Milestone 3
From lab specs: This milestone will extend the menu system from the previous
milestones, develops a function that loads another ETS file (stops.txt) into
a Python data structure, develops a function that allows a user to access
this data structure, and extends the graphical user interface to support the 
plotting of bus stops.
'''

def menu():
    '''
    This is the main function that calls the rest of the functions. This
    function displays a menu and waits for the user to make a selection,
    executes the selection, and displays the menu again until the exit
    selection is entered. This error checks to ensure that only valid integers
    are eneterd as menu selections.
    
    Parameter:
    Returns:
    None
    
    ex) menu()
    
            Edmonton Transit System
        ---------------------------------
        (1) Load shape IDs from GTFS file
        (2) Load shapes from GTFS file
        (3) Load stops from GTFS file
        
        (4) Print shape IDs for a route
        (5) Print points for a shape ID
        (6) Print Stops for a location
        
        (7) Save shapes, shape IDs, and stops in a pickle
        (8) Load shapes, shape IDs, and stops from a pickle
        
        (9) Display interactive map
        
        (0) Quit
    
    Enter command: a
    Enter command:  
    Enter command: avs
    Enter command: 3.5
    Enter command: 3
    Enter command: 0
    Goodbye
    '''
    while True:
        global menustr
        print(menustr)
        option = get_option()            
        if option == 1: shapeID = option1()
        if option == 2: shapes = option2()
        if option == 3: stops = option3(ftype="data/stops.txt")
        if option == 4: option4(shapeID)
        if option == 5: option5(shapes)
        if option == 6: option6(stops)
        if option == 7: option7(shapeID, shapes, stops)
        if option == 8: option8()
        if option == 9: Edmonton_GUI(shapeID, shapes, stops)
        if option == 0:
            print("Goodbye")
            break
    return None

def get_option():
    '''
    Helper function gets the user to enter the desired option. Error checks to
    ensure that it is a valid integer and one of the menu selections.
    
    Parameter:
    Returns:
    int - the menu choice selection that the user wants to perform
    
    ex) get_option()
    
    Enter command: a
    Enter command:  
    Enter command: avs
    Enter command: 3.5
    Enter command: 1   1
    Enter command: 1
    '''
    option = input("Enter command: ")
    while True:
        if len(option) == 1 and ('0' <= option <= '9'):
            return int(option)
        option = input("Enter command: ")
    return None

def option1():
    '''
    This is a function that executes option 1 of the menu options. It calls on
    other helper functions to open the file and extract the bus route numbers
    with their corresponding shape IDs from the file. 
    
    Parameter:
    Returns:
    dict - dictionary of the bus route numbers with corresponding shape IDs
    
    ex) option1()
    option1 = {'1': ['1-30-1', '1-32-1', '1-31-1', '1-33-1', '1-35-1',
    '1-36-1', '1-34-1', '1-37-1', '1-38-1', '1-39-1'],'10': ['10-20-1',
    '10-19-1', '10-18-1', '10-17-1', '10-44-1', '10-49-1', '10-51-1',
    '10-13-1', '10-45-1', '10-46-1', '10-47-1', '10-48-1', '10-50-1'],...}
    '''
    option1 = {}
    ftype = "data/trips.txt"
    fName = execute_file(ftype)
    while True:
        if fName == 'trips.txt':
            break
        print("Wrong file for this option!")
        fName = execute_file(ftype)
    shapeID = shape_ID1(fName)
    return shapeID
    
def shape_ID1(fName):
    '''
    Helper function that creates a dictionary of the bus routes and their
    corresponding Shape IDs. Uses for loops and lists to extract the correct
    information from the file and place them in the new dictionary.
    
    Parameter:
    str - file name that has already been checked if it is valid
    Returns:
    dict - dictionary of the bus route numbers with corresponding shape IDs
    '''
    option1 = {}
    file = open(fName, 'r')
    astring = file.read().replace('\n', ',')
    file.close()
    route, shapeID , alist = [], [], astring.split(',')
    for i in range(7,len(alist)-1,7): route.append(alist[i])
    for i in range(13,len(alist)-1,7): shapeID.append(alist[i])
    for i in range(len(route)-1):
        if route[i] in option1:
            info = option1.get(route[i])
            if shapeID[i] not in info: option1[route[i]].append(shapeID[i])
        else:
            option1[route[i]] = [shapeID[i]]
    return option1
    
def execute_file(ftype):
    '''
    This helper function asks the user for a file name and error checks using
    try and except to see if the file is missing, has an error, or corrupt.
    This also lets the user return the file name if there was nothing entered. 
    
    Parameter:
    str - type of file/ file name
    Returns:
    str - name of file
    
    ex)
    Enter a file name [data/trips.txt]: 0
    There was a problem opening 0!
    Enter a file name [data/trips.txt]:  
    There was a problem opening  !
    Enter a file name [data/trips.txt]: abd
    There was a problem opening abd!
    Enter a file name [data/trips.txt]: trips.txt
    '''
    while True:
        fName = input(f"Enter a file name [{ftype}]: ")
        try:
            if fName == '':
                if ftype == "data/trips.txt":
                    fName = "trips.txt" ; fIn = open(fName)
                    fIn.close()
                    return fName 
                if ftype == "data/shapes.txt":
                    fName = "shapes.txt" ; fIn = open(fName)
                    fIn.close()
                    return fName 
                if ftype == "data/stops.txt":
                    fName = "stops.txt" ; fIn = open(fName)
                    fIn.close()
                    return fName                 
            else:
                fIn = open(fName)
                fIn.close()
                return fName
        except Exception as e: print(f"There was a problem opening {fName}!")
            
def option4(shapeID):
    '''
    This function prompts the user for a route number and displays the
    corresponding shape IDs for the existing route number. If the route number
    does not exist, it will display that it is not found.
    
    Parameter:
    dict - dictionary of the bus route numbers with corresponding shape IDs
    Returns:
    None  
    
    ex)
    Route? ab35
    Shape IDs for ab35:
    ** NOT FOUND **
    
    Route? 1
    Shape IDs for 1:
            1-30-1
            1-32-1
            1-31-1
            1-33-1
            1-35-1
            1-36-1
            1-34-1
            1-37-1
            1-38-1
            1-39-1
    '''
    route = input("Route? ")
    if route not in shapeID:
        print(f"Shape IDs for {route}:\n** NOT FOUND **")
    else:
        print(f"Shape IDs for {route}:")
        for i in shapeID[route]:
            print("\t" + i)
    return None

def option2():
    '''
    This is a function that executes option 2 of the menu options. It calls on
    other helper functions to open the file and extract the shape IDs with their
    corresponding longitude and latitude pairs.
    
    Parameter:
    Returns:
    dict - dictionary of the shape IDs with their longitude and latitude pairs
    
    ex) option2()
    option1 = {'3-15-1': [['53.54026', '-113.59275'], ['53.54026', '-113.59383'],
    ['53.54078', '-113.59382'], ['53.54095', '-113.59382'], ['53.54103',
    '-113.59382'], ['53.54111', '-113.59384'], ['53.54123', '-113.59384'],
    ['53.54129', '-113.59386'], ['53.54129', '-113.59259'], ['53.54129',
    '-113.59032'], ['53.5436', '-113.59032'], ['53.54486', '-113.59034'],
    ['53.54636', '-113.59033'],...], '3-16-2': [...], ...}    
    '''
    ftype = "data/shapes.txt"
    fName = execute_file(ftype)
    while True:
        if fName == 'shapes.txt':
            break
        print("Wrong file for this option!")
        fName = execute_file(ftype)    
    shapes = shape_ID2(fName)
    return shapes

def shape_ID2(fName):
    '''
    Helper function that creates a dictionary of the shape IDs and their
    corresponding longitude and latitude pairs. Uses for loops and lists to 
    extract the correct information from the file and place them in the new
    dictionary.
    
    Parameter:
    str - file name that has already been checked if it is valid
    Returns:
    dict - dictionary of the shape IDs and their longitude and latitude pairs
    '''
    option2 = {}
    file = open(fName, 'r')
    astring = file.read().replace('\n', ',')
    file.close()
    alist = astring.split(',')
    shapeID = [alist[i] for i in range(4, len(alist), 4)]
    lat = [alist[i] for i in range(5, len(alist)-1, 4)]
    long = [alist[i] for i in range(6, len(alist)-1, 4)]
    for i in range(len(shapeID)-1):
        if shapeID[i] in option2:
            info, coord = option2.get(shapeID[i]), [lat[i], long[i]]
            if coord not in info: option2[shapeID[i]].append(coord)
        else:
            coord = [lat[i], long[i]]
            option2[shapeID[i]] = [coord]
    return option2

def option5(shapes):
    '''
    This function prompts the user for a shape ID and displays the corresponding 
    longitude and latitude pairs for the existing route number. If the route 
    number does not exist, it will display that it is not found.
    
    Parameter:
    dict - dictionary of the shape IDs with their longitude and latitude pairs
    Returns:
    None  
    
    ex)
    Shape ID? what is this?
    Shape for what is this?:
    ** NOT FOUND **

    Shape ID? 3-15-1
    Shape for 3-15-1:
	(53.54026, -113.59275)
	(53.54026, -113.59383)
	(53.54078, -113.59382)
	(53.54095, -113.59382)
	(53.54103, -113.59382)
	(53.54111, -113.59384)
	(53.54123, -113.59384)
	(53.54129, -113.59386)
	(53.54129, -113.59259)
	(53.54129, -113.59208)
        ...
    '''
    shapeID = input("Shape ID? ")
    if shapeID not in shapes:
        print(f"Shape for {shapeID}:\n** NOT FOUND **")
    else:
        print(f"Shape for {shapeID}:")
        stuff = shapes[shapeID]
        for i in stuff:
            pair = ", ".join(i)
            print(f"\t({pair})")
    return None

def option7(shapeID, shapes, stops):
    '''
    This function allows a user to enter a file name and pickle the three dicts
    (shapeID, shapes, stops) to that file name. If the user enters without
    entering a file name, it uses the default 'etsdata.p'.
    '''
    pklFname = input("Enter a file name [etsdata.p]: ")
    if pklFname == "": pklFname = 'etsdata.p'
    fPkl = open(pklFname, "wb")
    info = (shapeID, shapes, stops)
    pickle.dump(info, fPkl)
    fPkl.close
    
def option8():
    '''
    This function allows a user to enter a file name and loads the pickle file
    that contains the three dictionaries. If the user enters without entering
    a file name, it uses the default 'etsdata.p'.
    '''
    pklFname = input("Enter a file name [etsdata.p]: ")
    if pklFname == "": pklFname = 'etsdata.p'
    # PUT IN TRY AND EXCEPT HERE OR CONNECT IT TO EXECUTE_FILE()
    fPkl = open(pklFname, "rb")
    pickle.load(fPkl)
    #from_pkl = pickle.load(fPkl)       # Dev check
    #a, b = from_pkl
    #pprint(a) ; pprint(b)
    fPkl.close()

def option3(ftype="data/stops.txt"):
    '''
    This reads bus stop information from file fName, where each line is like:
       "1001,1001,"Abbottsfield Transit Centre",,  53.571965,-113.390362,,,0,"
        0   1    2                             34           5           678 9
         ID        name                           longitude   latitude
    and returns a dictionary with bus stop (long, lat) as keys, and a list of
    (bus stop ID, bus stop name) tuples for each; ex.:
    {  (53.571965, -113.390362) :  [ ('1001', 'Abbottsfield Transit Centre') ]
            :           :               :                  :                   }
    NOTE: examination of the resulting dictionary and source text file seems to
    indicate that there is a one to one relationship between the dictionary keys
    and bus stops in the text file, suggesting that there is no need for a list
    of bus stop info for each key.
    '''
    fName = execute_file(ftype)
    file = open(fName)
    lines = file.readlines()[1:]
    file.close()
    
    stops = {}                                  # Dictionary to be returned
    # Ex.
    #{  (53.571965, -113.390362) :  [ ('1001', 'Abbottsfield Transit Centre') ]
    #        :           :               :                  :                 }

    # Each line, ex. :
    #"1001,1001,"Abbottsfield Transit Centre",,  53.571965,-113.390362,,,0,"
    # 0   1    2                             34           5           678 9
    #  ID        name                           latitude   longitude    
    for line in lines:
        stuff = line.strip().split(',')
        stop_id, name = stuff[0], stuff[2]
        lat, long = float(stuff[4]), float(stuff[5])
        # Ex.
        #{(53.571965, -113.390362): [('1001', 'Abbottsfield Transit Centre')]
        stops[(lat, long)] = [(stop_id, name)]      # NOTE: unique coordinates
        
    return stops

def option6(stops):
    '''
    This function prompts the user for a location and displays the corresponding 
    stops and information for the given latitude and longitude. If the location
    does not have a stop, it will display that it is not found.
    
    Parameter:
    stops - dictionary of the stops and information
    Returns:
    None
    
    ex)
    Location as 'lat,lon'? 0,0
    Stops for (0.0, 0.0):
    ** NOT FOUND **

    Location as 'lat,lon'?  53.575137,-113.403388
    Stops for ( 53.575137,-113.403388):
        1065	40 Street & 121 Avenue
    '''
    latlon1 = input("Location as 'lat,lon'? ")
    latlon2 = latlon1.split(',')
    if len(latlon2) != 2:
        print(f"Stops for {latlon1}:\n** NOT FOUND **")
        return
    else: latlon3 = (float(latlon2[0]), float(latlon2[1]))
    alist = []
    for stop in stops.keys():
        if latlon3 != stop: pass
        else: alist += stops[stop]
    if alist != []:
        print(f"Stops for ({latlon1}):")
        for i in alist:
            info = i[1].strip('"')
            print(f"\t{i[0]}\t{info}")
    else: print(f"Stops for {latlon3}:\n** NOT FOUND **")
    return None

def haversine(lat1, lon1, lat2, lon2):
    '''
    Returns great-circle distances between two points on earth from their 
    longitudes and latitudes ( (lat1, lon1(, and (lat2, lon2) )
    From: https://rosettacode.org/wiki/Haversine_formula#Python  
    Ex. haversine(36.12, -86.67, 33.94, -118.40) = 2887.25995 (km)
    '''
    from math import radians, sin, cos, sqrt, asin
    R = 6372800             # Earth radius in meters
 
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
 
    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))
 
    return R * c    

def closest_stops(lat, long, stops, num=5):
    '''
    Given a dictionary of bus stops, ex.
    { (53.571965, -113.390362) : [('1001', 'Abbottsfield Transit Centre')] ... }
    and location (lat, long), this computes the distances from (lat, long) to
    all entries in stops, constructs a list of all these distances, which is 
    then sorted by distance, and returns a list of the first num; ex.: 
       closest_stops(53.57196, -113.3903, stops)
    returns a list of (num) lists [ distance, stop_id, stop_name, lat, long ]: 
     [ [  4.1, '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
       [ 21.3, '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
       ...
       [192.3, '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    '''
    d = []                                      # List of distances & infos
    for loc, info in stops.items():
        #                      loc : info
        # (53.571965, -113.390362) : [('1001', '"Abbottsfield Transit Centre"')]
        #      havesine(lat1, lon1, lat2  , lon2  )
        dist = haversine(lat, long, loc[0], loc[1])
        stop_name = info[0][1].strip('"')
        d.append([round(dist, 1)    , info[0][0], stop_name , loc[0], loc[1] ])
        #        [distance          , stop_id   , stop_name , lat   , long   ]
    fivestops = sorted(d)[:num]
    return fivestops

def print_closest_stops(fivestops):
    '''
    This expects a list of (nearest) bus stops, ex.:
      distance, stop_ID,  name                        , latitude , longitude 
           [0]      [1]   [2]                           [3]        [4]
    [[     4.1,  '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
     [    21.3,  '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
        ...
     [   192.3,  '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    and for each prints out the distance, bus stop id, and name.
    
    ex)
    Nearest stops:
          Distance   Stop   Description
            8285.5   6379   127 Street & Edmonton Young Offenders Centre
            8403.3   66113   127 Street & 184 Avenue
            8683.9   7410   Mons Avenue & Arras Avenue Garrison
            8843.4   7610   Biscay Street & Arras Avenue Garrison
            8864.1   7961   Biscay Street & Mons Avenue Garrison
    '''
    import sys
    print("Nearest stops:"
          f"\n{'Distance':>18}   Stop   Description")
    for i in fivestops:
        print(f"{i[0]:>18}   {i[1]}   {i[2]}")
    sys.stdout.flush()
    return None
    

#=============================================================================
# GUI Business

def btn_create(win, x, y, w, h, label):
    # Creates a Rectangle and centered Text, aand returns (Rectangle, Text)
    r = Rectangle(Point(x, y), Point(x+w, y+h)) ;   r.draw(win)
    r.setFill('white')
    t = Text(r.getCenter(), label) ;                t.draw(win)
    return r, t

def btn_clicked(pt, btn):
    # Returns True if Point pt is inside the boundaries of button btn
    # Recall: btn: (Rectangle, Text)
    p1, p2 = btn[0].getP1(), btn[0].getP2()    # Assuming p1, p2: UL, LR corners
    return (p1.x <= pt.x <= p2.x) and (p1.y <= pt.y <= p2.y)

def plot_route(route, win, shapeID, shapes):
    '''
    This plots the specified route, by joining all coordinates in shapes dict'y,
    using shape id's in shapeID dictionary.
    REFER to Lab *: plot monthly temperatures
    
    Parameters:
    route - the route number the user entered
    win - the window of the interactive map
    dict - dictionaries for shapeID and shapes
    Returns:
    '''   
    total, todraw = 0, []
    if route not in shapeID: return
    else:
        for shapeIDs in shapeID[route]:
            content = list(shapes[shapeIDs])
            if len(content) > total:
                total = len(content)
                todraw = shapes[shapeIDs]   
    for i in range(len(todraw)-1):
        pair1, pair2 = todraw[i], todraw[i+1]
        line = Line(Point(float(pair1[1]), float(pair1[0])),
                    Point(float(pair2[1]), float(pair2[0])))
        line.draw(win)
        line.setFill('gray50') ; line.setWidth(3)

def plot_stops(win, fivestops, long, lat, stops):
    '''
    This expects GraphWin, and a list of bus stops, ex.:
      distance, stop_ID,  name                        , latitude , longitude 
           [0]      [1]   [2]                           [3]        [4]
    [[     4.1,  '1001', 'Abbottsfield Transit Centre', 53.571965, -113.390362], 
     [    21.3,  '1002', 'Abbottsfield Transit Centre', 53.572087, -113.390058], 
        ...
     [   192.3,  '1612', '34 Street & 119 Avenue', 53.57185, -113.393205]  ]
    and plots a Point at each one.
    '''
    aPoint = Point(long, lat)            # Place Point where mouse clicked
    #aPoint.setWidth(4)                   # Doesn't work
    aPoint.setFill('red')
    aPoint.draw(win)
       
    for i in fivestops:
        aPoint = Point(i[4], i[3])            # Place Point where mouse clicked
        #aPoint.setWidth(4)                   # Doesn't work
        aPoint.setFill('black')
        aPoint.draw(win)
    print_closest_stops(fivestops)

def helperGUI(win, btn_Close, btn_Plot, user_entry, msg, shapeID, shapes, stops):
    '''
    This is a helper function that allows the user to interact with the map. It
    responds to the mouse clicks of the user and displays the coordinates of the
    clicks and it also plots the routes when a valid route is entered into the
    text box.
    
    Parameters:
    win - the window of the interactive map
    btn_Close, btn_Plot - the rectangle buttons that allow interactivity
    msg - message inside the button
    user_entry - grey box to enter the route
    dict - dictionaries for shapeID, shapes, and stops
    Returns:
    '''
    while True:                          #======================== MAIN GUI LOOP
        coords = win.getMouse()          # Get: Point(x, y): Point(long, lat)
        long, lat = coords.x, coords.y   # Geographical coords
        
        pt = win.toScreen(long, lat) ;   # toScreen() return: [x, y]
        pix = Point(pt[0], pt[1])        # To satisfy btn_clicked()
        if btn_clicked(pix, btn_Close):  # btn_clicked expects a pixel x, y
            btn_Close[1].setFill('red')
            btn_Close[1].setText('BYE BYE')
            break
        
        if btn_clicked(pix, btn_Plot):
            #Recall: btn_Plot: (Rectangle, Text)
            route = user_entry.getText()[:3]
            if route.isdigit():
                btn_Plot[1].setText(f"Bus: {route}")
                # plots the shape for that bus route with the most points
                plot_route(route, win, shapeID, shapes)
            else: btn_Plot[1].setText(f"No {route}")
            #btn_Plot[1].setFill('blue') 
        
        msg[1].setText(f"Lat: {lat:.3f}\nLong: {long:.3f}")
        #msg[1].setText(f"X: {pix.x}\nY: {pix.y}")        #  Dev check
        
        fivestops = closest_stops(lat, long, stops, num=5) 
        plot_stops(win, fivestops, long, lat, stops)        
    
def Edmonton_GUI(shapeID, shapes, stops):
    '''
    This is the main function that sets up the interactive map for Edmonton.
    It allows the user to click on the map to get the longitude and latitude
    coordinates. It also allows the user to draw the specific routes when
    a valid route is entered.
    
    Parameters:
    dict - dictionaries for shapeID, shapes, and stops
    Returns:
    '''
    img = Image(Point(0, 0,), giFname)
    w, h = img.getWidth() , img.getHeight()
    
    win = GraphWin("CMPT103-21W ETS BUS ROUTES (C) JETHRO INFANTE", w, h)
    img.move(w//2, h//2)
    img.draw(win)
    
    # Call syntax: (Rectangle, Text) = btn_create(win, x, y, h, label)
    btn_Close  = btn_create(win, w-100, 20, 70, 20, "CLOSE")
    btn_Plot   = btn_create(win, 100, 20, 70, 20, "PLOT")
    user_entry = Entry(Point(50, 30), 8) ;     user_entry.draw(win)
    user_entry.setFill('gray') ;               user_entry.setText('101')
    msg        = btn_create(win, w//2-75, 20, 150, 40, "MOUSE\nCLICK")

    # Change coordinates to geographical latitude and longitude (y, x)
    win.setCoords(LONG_L, LAT_L, LONG_R, LAT_U)       #xL, yL, xR, yU

    helperGUI(win, btn_Close, btn_Plot, user_entry, msg, shapeID, shapes, stops)
    
    win.getMouse()
    win.close()


#============================================================================
if __name__ == '__main__':
    print(TITLE)
    
    if input("Execute tests (y/n): ") in "Yy":
        
        print("\nMILESTONE ONE TEST CODE\n")
        print("    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 1\n"
              "Enter a file name [data/trips.txt]: \n"
              "There was a problem opening  !\n"
              "Enter a file name [data/trips.txt]: 32\n"
              "There was a problem opening 32!\n"
              "Enter a file name [data/trips.txt]: shapes.txt\n"
              "Wrong file for this option!\n"
              "Enter a file name [data/trips.txt]: trips.txt\n\n"
              
              "    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 4\n"
              "Route? 5ab3\n"
              "Shape IDs for 5ab3:\n"
              "** NOT FOUND **\n\n"
              
              "    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 4\n"
              "Route? 1\n"
              "Shape IDs for 1:\n"
              "        1-30-1\n"
              "        1-32-1\n"
              "        1-31-1\n"
              "        1-33-1\n"
              "        1-35-1\n"
              "        1-36-1\n"
              "        1-34-1\n"
              "        1-37-1\n"
              "        1-38-1\n"
              "        1-39-1\n\n"
              
              "    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 2\n"
              "Enter a file name [data/shapes.txt]: \n\n"
              
              "    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 5\n"
              "Shape ID? 3-15-1\n"
              "Shape for 3-15-1:\n"
              "        (53.54026, -113.59275)\n"
              "        (53.54026, -113.59383)\n"
              "        (53.54078, -113.59382)\n"
              "                 ...\n"
              "        (53.57006, -113.54971)\n"
              "        (53.57005, -113.54965)\n"
              "        (53.57004, -113.54958)\n\n"
              
              "    Edmonton Transit System\n"
              "---------------------------------\n"
              "(1) Load shape IDs from GTFS file\n"
              "(2) Load shapes from GTFS file\n\n"
              
              "(4) Print shape IDs for a route\n"
              "(5) Print points for a shape ID\n\n"
              
              "(0) Quit\n\n"
              
              "Enter command: 0\n"
              "Goodbye")
        
        
        # EXLPORING PICKLE
        
        # Put stuff in file using pickle.dump()
        '''
        fPkl = open("Stuff.pkl", "wb")
        x = 4
        names = ['Sam', 'Rik', 'Sue', 'Jane', 'Bob']
        scores = [23, 45, 67, 78, 89, 21, 32, 43]
        story = "Flying Pickle Alert!!! Pickle file can be hacked"
        stuff = (x, names, scores, story)
        pickle.dump(stuff, fPikl)
        fPikl.close
        '''
        # Load the contents of the file using pickle.load()
        '''
        fPkl = open("Stuff.pkl", "rb")
        from_pkl = pickle.load(fPkl)
        print(len(from_pkl))
        a, b, c, d = from_pkl
        print(a) ; print(b) ; print(c) ; print(d)
        fPkl.close()
        '''
        # Exploring more pickle
        '''
        pklFname = "Cmpt103W21_ETS_data.pkl"
        fPkl = open(pklFname, 'rb')
        jazz = pickle.load(fPkl)
        pickle.dump((shapeID, "shapes_dict"), fPkl)
        print(jazz[0])
        fPkl.close()
        '''
        
        # TESTING MILESTONE 3
        print("\n\nTesting: option3('data/stops.txt')")
        stops = option3(ftype="data/stops.txt")
        for stop in list(stops.keys())[:5]: print(stop, stops[stop])        
        
        print("\n\nTesting: option6(stops)\n"
              "Location as 'lat,lon'? 0,0\n"
              "Stops for (0.0, 0.0):\n"
              "** NOT FOUND **\n"
              "\n"
              "Location as 'lat,lon'?  53.575137,-113.403388\n"
              "Stops for ( 53.575137,-113.403388):\n"
              "        1065	40 Street & 121 Avenue")
        
        print(f"\n\nTest: haversine(36.12, -86.67, 33.94, -118.40) = "
              f"{round(haversine(36.12, -86.67, 33.94, -118.40), 3)} km")
       
        print("\n\nTesting: closest_stops(53.57196, -113.3903, stops)")
        closest_stops = closest_stops(53.57196, -113.3903, stops)
        pp(closest_stops, 120)
        
    else:
        menu()