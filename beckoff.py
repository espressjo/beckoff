#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 09:40:04 2021

@author: noboru
"""

from opcua import Client,ua
import traceback

class beckoff():
    '''
        small example class to read/write varible on a beckoff PLC.
    '''
    def __init__(self,ip):
        self.ip_addr = ip
        self.port = 4840
        self.beck = None
        self.node = 'MAIN.Filter%d.stat' #node to read a Filter# variable (stat)
        self.node_lr_position = 'MAIN.Filter%d.ctrl.lrPosition' #node to change the lrPosition of Filter 1 or 2
    def connect(self):
        '''
            Open a connection with the PLC. Must be called 1st. If with statement is used, no need to use this function.
        '''
        self.beck = Client("opc.tcp://%s:%d"%(self.ip_addr,self.port))
        self.beck.connect()
        root=self.beck.get_root_node()
        print(":::::root:::::")
        print(root)
        objects = self.beck.get_objects_node()
        print(":::::objects:::::")
        print(objects)
        child = objects.get_children()
        print(":::::child:::::")    
        print(child)
    def _read_Filter(self,var,filter_nb):
        '''
            This function will return the value (str format) of varible [var] of ND filter # [filter_nb]
        '''
        #print(var)
        val1 = self.beck.get_node("ns=4; s=%s.%s"%(self.node%filter_nb,var)).get_value()
        out = str(val1).strip()
        return out
    def _read_var(self,var,node):
        #print(var)
        '''
            return value for variable [var] on specified [node]
        '''
        val1 = self.beck.get_node("ns=4; s=%s"%(".".join([node,var]))).get_value()
        out = str(val1).strip()
        return out
    def rFilter1(self):
        '''
            Return position of encoder in float of ND filter 1
        '''
        pos = self._read_Filter('lrPosActual',1)
        if isinstance(pos,str):
            return float(pos)
        else:
            return None
    def disconnect(self):
        '''
            Close opcua connection with beckoff.
        '''
        self.beck.disconnect()
        return
    def rFilter2(self):
        '''
            Return position of encoder in float of ND filter 2
        '''
        pos = self._read_Filter('lrPosActual',2)
        if isinstance(pos,str):
            return float(pos)
        else:
            return None
    def _set_Filter_lrPosition(self,filter_nb,pos):
        '''
            Will set the lrPosition variable [pos] for ND filter # [filter_nb]
            [pos] can be an integer, str or float.
        '''
        if filter_nb!=1 and filter_nb!=2:
            print("filter_nb must be 1 or 2")
            return
        dv = ua.DataValue(ua.Variant(float(pos), ua.VariantType.Double))
        var = self.beck.get_node("ns=4;  s=%s"%(self.node_lr_position%filter_nb))
        var.set_data_value(dv)
        return
    def __enter__(self):
        '''
            Since connection to hardware is made, its better to use with statement i.e., with beckoff("192.168.62.150") as beck: ...
        '''
        self.connect()
        return self
    #def __exit__(self):
    #    self.disconnect()
    def __exit__(self, exc_type, exc_value, tb):
        self.beck.disconnect()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through

        return True
    
if '__main__' in __name__:
    #example for beckoff com
    
    #open the connection with PLC
    with beckoff("192.168.62.150") as beck:
        #read position of ND filter 1
        print(beck.rFilter1())
        
        #read position of ND filter 2
        print(beck.rFilter2())
        
        #write lrPosition varible for ND filter #2
        beck._set_Filter_lrPosition(2,92711)
        
    # connection is automatically closed.
    
    
    