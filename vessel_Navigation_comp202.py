#program that handles a boats navigation system.
#takes user input about the coordinates and the dimensions of the boat.
#tells user if boat approching a dangerous location

import math
import random

MIN_LAT = -90 #latitude is angle between -90 and +90 degrees
MAX_LAT = 90
MIN_LONG = -180 #longitude is angle between -180 & 180 degrees
MAX_LONG = 180
EARTH_RADIUS = 6371 #in kilometer


def meter_to_feet(meter):
    '''returns feet from meter value
    Parameters:
        meter: a number(positive float)
    Returns:
        feet: a number(float) #it is rounded to 2 decimals

    Examples:
    >>>meter_to_feet(65)
    213.3
    >>>meter_to_feet(4)
    13.12
    >>>meter_to_feet(11)
    36.08
     '''
    feet_conversion_factor = 3.28
    feet = round(meter*feet_conversion_factor,2)
    return feet
    
def degrees_to_radians(degrees):
    """
    Converts an angle from degrees to radians.
    Parameters:
    - degrees (float): The angle in degrees to be converted to radians.
    Returns:
    radians(float): The equivalent angle in radians, rounded to two decimal places.

    Examples:
    >>> degrees_to_radians(90)
    1.57
    >>> degrees_to_radians(180)
    3.14
    >>> degrees_to_radians(45)
    0.79
    """
    radians=round(degrees*math.pi/180,2)
    return radians

def get_vessel_dimensions():
    """
    Retrieves and converts the dimensions of a vessel from meters to feet.
    Parameter: None
    Returns:
    lenght_feet, width_feet (tuple): A tuple containing the vessel length and width in feet.

    Examples:
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 10
    Enter the vessel width (in meter): 5
    (32.81, 16.4)
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 15.2
    Enter the vessel width (in meter): 8.7
    (49.87, 28.54)
    >>> get_vessel_dimensions()
    Enter the vessel length (in meter): 7.5
    Enter the vessel width (in meter): 3.3
    (24.61, 10.83)
    """
    length = float(input("Enter the vessel length (in meter): "))
    width = float(input("Enter the vessel width (in meter): "))
    length_feet=round(meter_to_feet(length),2)
    width_feet=round(meter_to_feet(width),2)
    return length_feet, width_feet

def get_valid_coordinate(val_name, min_float, max_float):
    """
    asks user to enter a coordinate within a specified range.

    Parameters:
    - val_name (str): The name of the coordinate value, used in user prompts.
    - min_float (float): The minimum allowed value for the coordinate.
    - max_float (float): The maximum allowed value for the coordinate.

    Returns:
    float: The valid numerical coordinate entered by the user.

    Examples:
    >>> get_valid_coordinate("latitude", -90.0, 90.0)
    What is your latitude? 91
    Invalid latitude
    What is your latitude? 45
    45.0

    >>> get_valid_coordinate("longitude", -180.0, 180.0)
    What is your longitude? -200
    Invalid longitude
    What is your longitude? 120
    120.0

    >>> get_valid_coordinate("altitude", 0.0, 5000.0)
    What is your altitude? 5500
    Invalid altitude
    What is your altitude? 3000.5
    3000.5
    """
    value=None   #figure out how to chnage name in output val_nmae
    while value==None or not(min_float < value < max_float):
        try:
            value=float(input("What is your "+val_name+" ?"))
            if not (min_float < value < max_float):
                print("Invalid "+val_name )
        except ValueError:
            print("ERROR")
    return value

def get_gps_location():
    """
    asks the user to enter valid latitude and longitude coordinates for a GPS location.
    Parameneter: none
    Returns:
    latitude, longitude(tuple): the valid latitude and longitude coordinates.

    Examples:
    >>> get_gps_location()
    What is your latitude? 91
    Invalid latitude
    What is your latitude? 45.123
    What is your longitude? -200
    Invalid longitude
    What is your longitude? 120.456
    (45.123, 120.456)
    >>> get_gps_location()
    What is your latitude? 35.789
    What is your longitude? 190
    Invalid longitude
    What is your longitude? -73.456
    (35.789, -73.456)
    >>> get_gps_location()
    What is your latitude? -95
    Invalid latitude
    What is your latitude? 25.678
    What is your longitude? 98.765
    (25.678, 98.765)
    """
    latitude=get_valid_coordinate("latitide",MIN_LAT, MAX_LAT)
    longitude=get_valid_coordinate("longitide",MIN_LONG, MAX_LONG)
    
    return latitude, longitude

def distance_two_points(lat1,long1,lat2,long2):
    """
    Calculates distance bwt two points on the Earth's surface using Haversine formula.

    Parameters:
    - lat1 (float): Latitude of the first point in degrees.
    - long1 (float): Longitude of the first point in degrees.
    - lat2 (float): Latitude of the second point in degrees.
    - long2 (float): Longitude of the second point in degrees.

    Returns:
    distance(float): The distance between the two points in kilometers,
    #rounded to two decimal places.

    Examples:
    >>> distance_two_points(34.0522, -118.2437, 37.7749, -122.4194)
    559.27

    >>> distance_two_points(-33.8679, 151.2074, 40.7128, -74.0060)
    15965.33

    >>> distance_two_points(51.5074, -0.1278, 48.8566, 2.3522)
    1055.04
    """
    lat1_rad=degrees_to_radians(lat1)
    long1_rad=degrees_to_radians(long1)
    lat2_rad=degrees_to_radians(lat2)
    long2_rad=degrees_to_radians(long2)
              
              
    distance_lat=lat2_rad-lat1_rad
    distance_long=long2_rad-long1_rad
              
              #haversine formula
              
    a=math.sin(distance_lat/2)**2+math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(distance_long/2)**2
    c=2* math.atan2(math.sqrt(a), math.sqrt(1-a))
              
    distance_kms=EARTH_RADIUS*c
              
    return round(distance_kms, 2)

def check_safety(vessel_latitude,vessel_longitude):
    """
    Checks the safety of vessel navigation based on its coordinates.

    Parameters:
    - vessel_latitude (float): Latitude of the vessel in degrees.
    - vessel_longitude (float): Longitude of the vessel in degrees.

    Returns:
    it Prints a safety message based on the vessel's location.

    Examples:
    >>> check_safety(34.0522, -118.2437)
    Safe navigation.

    >>> check_safety(40.7306, -73.9352)
    Warning: Hazardous area! Navigate with caution.

    >>> check_safety(25.7617, -80.1918)
    Error: Restricted zone!
    """
    distance_restricted=distance_two_points(vessel_latitude,vessel_longitude,25,-71)
    if distance_restricted <= 400:
        print("Error: Restricted zone!")
    else:
        if 40< vessel_latitude <41 and -71 <vessel_longitude <-70:
            print("Warning: Hazardous area! Navigate with caution.")
        else:
            print("Safe navigation.")
            
def get_max_capacity(length, width):
    """
    Calculates the max people capacity based on vessles length and width.

    Parameters:
    - length (float): Length of the vessel in meters.
    - width (float): Width of the vessel in meters.

    Returns:
    capacity(int): The max capacity, rounded down to the nearest integer.

    Examples:
    >>> get_max_capacity(20, 8)
    10

    >>> get_max_capacity(30, 10)
    26

    >>> get_max_capacity(40, 12)
    36
    """
    if length<=26:
        capacity=length*width/15
    else:
        capacity=length*width/15 + (length - 26)*3
    
    return int(capacity)

def passengers_on_boat(length, width, num_passengers):
    """
    Checks if the number of passengers can fit and be distributed properly on vessel.

    Parameters:
    - length (float): Length of the boat in feet.
    - width (float): Width of the boat in feet.
    - num_passengers (int): Number of passengers attempting to board.

    Returns:
    bool: True if the passengers can safely board, False otherwise.

    Examples:
    >>> passengers_on_boat(20, 8, 12)
    True

    >>> passengers_on_boat(30, 10, 30)
    False

    >>> passengers_on_boat(40, 12, 16)
    True
    """
    if num_passengers<=get_max_capacity(length,width) and num_passengers%4==0:
            return True
    else:
        return False

def update_coordinate(position, min_float, max_float):
    """
    Updates a coordinate position with a random step.

    Parameters:
    - position (float): The current coordinate position.
    - min_float (float): The minimum allowed value for the coordinate.
    - max_float (float): The maximum allowed value for the coordinate.

    Returns:
    new_position(float): The updated coordinate position, rounded to two decimal places.

    Examples:
    >>> update_coordinate(50.0, 40.0, 60.0)
    54.82

    >>> update_coordinate(25.0, 20.0, 30.0)
    23.45

    >>> update_coordinate(0.0, -5.0, 5.0)
    -1.23
    """
    random.seed(123)
    
    while True:
        step=random.uniform(-10,10)
        
        new_position=position+step
        
        if min_float<new_position<max_float:
            return round(new_position,2)

        
def wave_hit_vessel(latitude, longitude):
    """
    Simulates the impact of waves on a vessel's coordinates,
    updating the position and checking safety.

    Parameters:
    - latitude (float): Current latitude of the vessel.
    - longitude (float): Current longitude of the vessel.

    Returns:
    new_latitude,new_longitude(tuple): A tuple containing the updated latitude and longitude
    

    Examples:
    >>> wave_hit_vessel(34.0522, -118.2437)
    Safe navigation.
    (34.72, -118.07)

    >>> wave_hit_vessel(40.7306, -73.9352)
    Warning: Hazardous area! Navigate with caution.
    (40.44, -74.22)

    >>> wave_hit_vessel(25.7617, -80.1918)
    Error: Restricted zone!
    (25.57, -79.88)
    """
    new_latitude = update_coordinate(latitude, MIN_LAT, MAX_LAT)
    new_longitude = update_coordinate(longitude, MIN_LONG, MAX_LONG)
    
    check_safety(new_latitude, new_longitude)    
    return new_latitude, new_longitude

def vessel_menu():
    """
    Displays a boat menu and provides options to check safety, maximum capacity, 
    update position, or exit.

    Menu Options:
    1. Check the safety of the boat based on its current coordinates.
    2. Check the maximum number of people that can fit on the boat based on its dimensions.
    3. Update the position of the boat, simulating the impact of waves.
    4. Exit the boat menu.

    Returns:
    None: Prints information based on the selected menu option.

    Examples:
    >>>Welcome to the boat menu!
    What is your latitude ?45.0888
    What is your longitude ?-73.232
    Your current position is at latitude 45.0888 and longitude -73.232
    Enter the vessel length (in meter): 34
    Enter the vessel width (in meter): 32
    Your boat measures 111.52 feet by 104.96 feet
    Please select an option below: 
    1. Check the safety of your boat
    2. Check the maximum number of people that can fit on the boat
    3. Update the position of your boat
    4. Exit boat menu
    Enter the number corresponding to your choice: 1
    Safe navigation.

    >>>Welcome to the boat menu!
    What is your latitude ?234
    What is your longitude ?32
    Your current position is at latitude 234.0 and longitude 32.0
    Enter the vessel length (in meter): 4
    Enter the vessel width (in meter): 54
    Your boat measures 13.12 feet by 177.12 feet
    Please select an option below: 
    1. Check the safety of your boat
    2. Check the maximum number of people that can fit on the boat
    3. Update the position of your boat
    4. Exit boat menu
    Enter the number corresponding to your choice: 2
    Enter the number of adults: 34
    Your boat can hold 34 adults

    >>>Welcome to the boat menu!
    What is your latitude ?2413
    What is your longitude ?421
    Your current position is at latitude 2413.0 and longitude 421.0
    Enter the vessel length (in meter): 23
    Enter the vessel width (in meter): 65
    Your boat measures 75.44 feet by 213.2 feet
    Please select an option below: 
    1. Check the safety of your boat
    2. Check the maximum number of people that can fit on the boat
    3. Update the position of your boat
    4. Exit boat menu
    Enter the number corresponding to your choice: 4
    End of boat menu.
    """
    print("Welcome to the boat menu!")
    
    latitude=float(input("What is your latitude ?"))
    longitude=float(input("What is your longitude ?"))
    
    print("Your current position is at latitude "+str(latitude)+" and longitude "+str(longitude))
    length, width= get_vessel_dimensions()
    
    print("Your boat measures "+str(length)+" feet by "+str(width)+" feet")
    
    menu=True
    while menu:
        print("Please select an option below: ")
        print("1. Check the safety of your boat")
        print("2. Check the maximum number of people that can fit on the boat")
        print("3. Update the position of your boat")
        print("4. Exit boat menu")
        
        choice = input("Enter the number corresponding to your choice: ")
        
        if choice == '1':
            # Option 1: Check the safety of the boat
            check_safety(float(latitude), float(longitude))
            
            
        elif choice == '2':
            # Option 2: Check the maximum number of people
            num_adults = int(input("Enter the number of adults: "))
            capacity = get_max_capacity(length, width)
            
            if num_adults > capacity:
                print("Your boat canot hold "+str(num_adults)+" adults")
            else:
                print("Your boat can hold "+str(num_adults) +" adults")   
            
        elif choice == '3':
            #Option 3: Update the position of the boat
            new_latitude, new_longitude=wave_hit_vessel(float(latitude),float(longitude))
            latitude=new_latitude
            longitude=new_longitude
            print("Your new position is latitude of "+str(latitude)+" and longitude of "+str(longitude))
            
        
        elif choice == '4':
            # Option 4: Exit the menu
            print("End of boat menu.")
            menu=False
        
        else:
            # Invalid choice
            print("Invalid choice. Please enter a valid option.")
