from enum import Enum

class CommunicatorAppMessageTypes(Enum):
    LOCATION = "LOCATION"        
    LOCATIONBOTTOM = "LOCATIONBOTTOM"
    ISLOCATION = "ISLOCATION"
    ISLOCATIONBOTTOM = "ISLOCATIONBOTTOM"
    ISDISTANCE = "ISDISTANCE"
    TEXTMESSAGE = "TEXTMESSAGE"

# define your own message types
class GPSHandlerAppMessageTypes(Enum):
    LOCATION = "LOCATION"    
    LOCATIONBOTTOM = "LOCATIONBOTTOM"
    DISTANCE = "DISTANCE"

nodeGPSLocations = [
    [20,10],
    [40,30],
    [95,45],
    [30,70]
]