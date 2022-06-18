import os
import sys
import time

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *
from adhoccomputing.Experimentation.Topology import Topology
#from adhoccomputing.Networking.LinkLayer.GenericLinkLayer import GenericLinkLayer
#from adhoccomputing.Networking.NetworkLayer.GenericNetworkLayer import GenericNetworkLayer
#from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from adhoccomputing.Networking.PhysicalLayer.UsrpB210OfdmFlexFramePhy import  UsrpB210OfdmFlexFramePhy
from adhoccomputing.Networking.ApplicationLayer.MessageSegmentation import *
from csmaPlain import CsmaPlain, CsmaPlainConfigurationParameters
from gpsHandler import *
from communicator import *
import logging

macconfig = CsmaPlainConfigurationParameters(-70)
sdrconfig = SDRConfiguration(freq =915000000.0, bandwidth = 2000000, chan = 0, hw_tx_gain = 70, hw_rx_gain = 20, sw_tx_gain = -12.0)

class AdHocNode(GenericModel):

    def on_init(self, eventobj: Event):
        print(f"Initializing {self.componentname}.{self.componentinstancenumber}")
        pass

    def on_message_from_top(self, eventobj: Event):
        self.send_down(eventobj)

    def on_message_from_bottom(self, eventobj: Event):
        self.send_up(eventobj)

    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        print("main: init")
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        
        #SubComponents
        self.gpsApp = GPSHandlerApp("GPSHandlerApp", componentinstancenumber, topology=topology)
        self.appl = CommunicatorApp("CommunicatorApp", componentinstancenumber, topology=topology)
        self.seg = MessageSegmentation("MessageSegmentation", componentinstancenumber, topology=topology)
        self.phy = UsrpB210OfdmFlexFramePhy("UsrpB210OfdmFlexFramePhy", componentinstancenumber, topology=topology, usrpconfig = sdrconfig)
        self.mac = CsmaPlain("MacCsmaPPersistent", componentinstancenumber,  configurationparameters=macconfig, sdr=self.phy.sdrdev, topology=topology)

        self.components.append(self.gpsApp)
        self.components.append(self.appl)
        self.components.append(self.mac)
        self.components.append(self.seg)
        self.components.append(self.phy)
        
        # SubComponent Connections
        self.gpsApp.connect_me_to_component(ConnectorTypes.PEER, self.appl) 

        self.appl.connect_me_to_component(ConnectorTypes.PEER, self.gpsApp)
        self.appl.connect_me_to_component(ConnectorTypes.DOWN, self.seg)

        self.seg.connect_me_to_component(ConnectorTypes.UP, self.appl)
        self.seg.connect_me_to_component(ConnectorTypes.DOWN, self.mac)
        
        self.mac.connect_me_to_component(ConnectorTypes.UP, self.seg)
        self.mac.connect_me_to_component(ConnectorTypes.DOWN, self.phy)
        
        self.phy.connect_me_to_component(ConnectorTypes.UP, self.mac)
        self.phy.connect_me_to_component(ConnectorTypes.DOWN, self)        

def main():
    print("main")
    topo = Topology()
    topo.construct_winslab_topology_without_channels(4, AdHocNode)
    topo.start()    

    i = 0
    while(i < 1):
        j = 0
        while(j < 4):
            #topo.nodes[3].appl.send_self(Event(topo.nodes[0], UsrpApplicationLayerEventTypes.STARTBROADCAST, None))
            topo.nodes[j].appl.send_self(Event(topo.nodes[0], CommunicatorAppEventTypes.STARTGPSREQ, None))
            time.sleep(5)
            j = j + 1
        i = i + 1
    
    print("END")

if __name__ == "__main__":
    main()