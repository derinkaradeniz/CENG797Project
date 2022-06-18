import time
import random
import math

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *
from common import *

class GPSHandlerAppMessageHeader(GenericMessageHeader):
    pass

class GPSHandlerAppEventTypes(Enum):
    pass

class GPSHandlerApp(GenericModel):
    myLocation = [0]*2
    def on_init(self, eventobj: Event):
        #print("gps: on init")
        self.counter = 0       
    
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        #print("gps: init")
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)

    def gpsLocator(self):
        self.myLocation[0] = nodeGPSLocations[int(self.componentinstancenumber)][0]
        self.myLocation[1] = nodeGPSLocations[int(self.componentinstancenumber)][1]

    def on_message_from_peer(self, eventobj: Event):
        #print("gps: from peer")

        self.myLocation[0] = random.random() * 100 - 50
        self.myLocation[1] = random.random() * 100 - 50
        #self.gpsLocator()
        if eventobj.eventcontent.header.messagetype is CommunicatorAppMessageTypes.ISLOCATION: 
            #print("gps: from peer: islocation") 
            header = GPSHandlerAppMessageHeader(GPSHandlerAppMessageTypes.LOCATION, self.componentinstancenumber, eventobj.eventcontent.header.messagefrom)     
            payload = self.myLocation
            message = GenericMessage(header, payload)
            evt = Event(self, EventTypes.MFRP, message)
            self.send_peer(evt)
        elif eventobj.eventcontent.header.messagetype is CommunicatorAppMessageTypes.ISLOCATIONBOTTOM:
            #print("gps: from peer: islocationbottom") 
            header = GPSHandlerAppMessageHeader(GPSHandlerAppMessageTypes.LOCATIONBOTTOM, self.componentinstancenumber, eventobj.eventcontent.header.messagefrom)     
            payload = self.myLocation
            message = GenericMessage(header, payload)
            evt = Event(self, EventTypes.MFRP, message)
            self.send_peer(evt)
        elif eventobj.eventcontent.header.messagetype == CommunicatorAppMessageTypes.ISDISTANCE:
            #print("gps: from peer: isdistance")
            nodeLocation = eventobj.eventcontent.payload
            distance = math.sqrt((self.myLocation[0] - nodeLocation[0])**2 + (self.myLocation[1] - nodeLocation[1])**2)
            print(f"{self.componentname}.{self.componentinstancenumber}: My location: {self.myLocation[0]},{self.myLocation[1]} ")
            print(f"{self.componentname}.{self.componentinstancenumber}: Node location: {nodeLocation[0]},{nodeLocation[1]} ")

            header = GPSHandlerAppMessageHeader(GPSHandlerAppMessageTypes.DISTANCE, self.componentinstancenumber, eventobj.eventcontent.header.messagefrom)     
            payload = distance
            message = GenericMessage(header, payload)
            evt = Event(self, EventTypes.MFRP, message) 
            self.send_peer(evt)
            print(f"{self.componentname}.{self.componentinstancenumber}: My distance from {eventobj.eventcontent.header.messagefrom} is {str(distance)}")
        else:
            print(f"{self.componentname}.{self.componentinstancenumber}: gps: from peer: nothing")