import time, random, math

from adhoccomputing.Generics import Event, EventTypes
from adhoccomputing.Networking.MacProtocol.GenericMAC import GenericMac, GenericMacEventTypes

class ComponentConfigurationParameters():
    pass

class CsmaPlainConfigurationParameters (ComponentConfigurationParameters):
    def __init__(self, cca_threshold = -35):
        self.cca_threshold = cca_threshold

class CsmaPlain(GenericMac):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None, sdr=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology, sdr)
        self.cca_threshold = configurationparameters.cca_threshold
    
    def on_init(self, eventobj: Event):
        self.retrialcnt = 0
        super().on_init(eventobj)

    def handle_frame(self): 
        if self.framequeue.qsize() > 0:
            clearmi, powerdb  = self.sdrdev.ischannelclear(threshold=self.cca_threshold)
            if  clearmi == True:
                try:
                    eventobj = self.framequeue.get()
                    evt = Event(self, EventTypes.MFRT, eventobj.eventcontent)
                    self.send_down(evt)
                    self.retrialcnt = 0
                except Exception as e:
                    logger.critical(f"MacCsmaPPersistent handle_frame exception {e}")
            else:
                self.retrialcnt = self.retrialcnt + 1
                print(f"retrial: {self.retrialcnt}")
                rand = random.random()
                backoffCount = math.ceil(rand*(2*self.retrialcnt-1))
                time.sleep(backoffCount*0.001)
        else:
            pass
        time.sleep(0.00001)
        self.send_self(Event(self, GenericMacEventTypes.HANDLEMACFRAME, None))