
# Import module
from tkinter import *
import xml.etree.ElementTree as ET
import sys
import os

# global lists

# Dropdown menu Port_Names
Port_Names = []
  
# Dropdown menu Pin_Numbers
Pin_Numbers = []
    
# Dropdown menu Pin_Options
Pin_Options = []  

clicked_Ports = []
clicked_Pins = []
clicked_Pin_Options = []

# Loaded Data 
loaded_Ports = []
loaded_Pins = []
loaded_Pin_Options = [] 
loaded2_Ports = []
loaded2_Pins = []
loaded2_Pin_Options = []
LoadedPortsIndication = 0
#Global Ports 
ELements_PORT_A = []
ELements_PORT_B = []
ELements_PORT_C = []
ELements_PORT_D = []
# Create object
root = Tk()
NumberOfConfiguredPorts = 0 
Row_index = 5   
Column_index = 0   
# Adjust size
root.geometry( "900x900" )

def options_parser():
    mytree = ET.parse('Options.jml')
    myroot = mytree.getroot()
    for x in myroot.iter('Option'):
        Pin_Options.append(x.text)


def pins_parser():
    mytree = ET.parse('Pins.jml')
    myroot = mytree.getroot()
    for x in myroot.iter('pinsNumber'):
        Pin_Numbers.append(x.text)

def ports_parser():
    mytree = ET.parse('Ports.jml')
    myroot = mytree.getroot()
    for x in myroot.iter('portName'):
        Port_Names.append(x.text)

def input_jmls_Parser():
    ports_parser()
    pins_parser()
    options_parser()

def Generate():
    child = ["0","0","0"]
    cnt = 0
    f_Generate = open("DIO_CFG.h", "w")
    f_Generate.writelines("#ifndef DIO_CFG_H\n")
    f_Generate.writelines("#define DIO_CFG_H\n\n")
    mytree = ET.parse('DIO_CFG.jml')
    myroot = mytree.getroot()
    for x in myroot.iter():
        if (x.tag != "jml"):
            if (x.tag != "PIN_CFG"):
                print(x.text)
                child[cnt] = x.text
                cnt += 1
            if (cnt == 3 ):
                f_Generate.writelines("#define\t"+child[0]+"_"+child[1]+"\t\t"+child[2]+"\n")
                cnt = 0      
    f_Generate.writelines("\n\n#endif\n") 
    f_Generate.close()

def load():
    global LoadedPortsIndication
    global root
    if (LoadedPortsIndication == 0):
        LoadedPortsIndication = 1
        root.destroy()
        root = Tk()
        root.geometry( "900x900" )
        main()
    cnt = 0
    Gen_cnt = 0
    global Row_index
    global Column_index
    global NumberOfConfiguredPorts
    Row_index = 0
    Column_index = 0
    # datatype of menu text
    global clicked_Ports
    global clicked_Pins
    global clicked_Pin_Options
    mytree = ET.parse('DIO_CFG.jml')
    myroot = mytree.getroot()
    for x in myroot.iter():
        if (x.tag != "jml"):
            if (x.tag != "PIN_CFG"):
                cnt += 1
                if(cnt == 1) : 
                    loaded_Ports[Gen_cnt]  =  x.text 
                if(cnt == 2) : 
                    loaded_Pins[Gen_cnt]  =  x.text 
                if(cnt == 3) : 
                    loaded_Pin_Options[Gen_cnt]  =  x.text
                    cnt = 0
                    Gen_cnt += 1
    print(Gen_cnt)
    for i in range (Gen_cnt):
        Row_index += 1
        print(loaded_Ports[i])
        print(loaded_Pins[i])
        print(loaded_Pin_Options[i])
        clicked_Ports[i] = StringVar()
        clicked_Pins[i] = StringVar()
        clicked_Pin_Options[i] = StringVar()
        
        # initial menu text
        clicked_Ports[i].set( loaded_Ports[i] )
        clicked_Pins[i].set( loaded_Pins[i] )
        clicked_Pin_Options[i].set( loaded_Pin_Options[i] )
        
        # Create Dropdown menu
        Column_index =0
        drop_ports = OptionMenu( root , clicked_Ports[i] , *Port_Names )
        drop_ports.grid(row=Row_index, column=Column_index)  
    
        # Create Dropdown menu
        Column_index += 5
        drop_pins = OptionMenu( root , clicked_Pins[i] , *Pin_Numbers )
        drop_pins.grid(row=Row_index, column=Column_index) 
    
        # Create Dropdown menu
        Column_index += 5
        drop_pins_Options = OptionMenu( root , clicked_Pin_Options[i] , *Pin_Options )
        drop_pins_Options.grid(row=Row_index, column=Column_index)
    NumberOfConfiguredPorts = Gen_cnt
        
def Save():
    global clicked_Ports
    global clicked_Pins
    global clicked_Pin_Options
    root = ET.Element("jml")
    for i in range (NumberOfConfiguredPorts):
        PORT = ET.SubElement(root, "PIN_CFG")
        ET.SubElement(PORT, "Port_Name").text = clicked_Ports[i].get()
        ET.SubElement(PORT, "PIN_Number").text = clicked_Pins[i].get()
        ET.SubElement(PORT, "PIN_Option").text = clicked_Pin_Options[i].get()
    tree = ET.ElementTree(root)
    tree.write("DIO_CFG.jml")

# Change the label text
def show():
    global Row_index
    global Column_index
    global NumberOfConfiguredPorts
    Row_index += 1
    # datatype of menu text
    global clicked_Ports
    global clicked_Pins
    global clicked_Pin_Options
    clicked_Ports[NumberOfConfiguredPorts] = StringVar()
    clicked_Pins[NumberOfConfiguredPorts] = StringVar()
    clicked_Pin_Options[NumberOfConfiguredPorts] = StringVar()
    
    # initial menu text
    clicked_Ports[NumberOfConfiguredPorts].set( "SELECT A port " )
    clicked_Pins[NumberOfConfiguredPorts].set( "SELECT A pin " )
    clicked_Pin_Options[NumberOfConfiguredPorts].set( "SELECT A pin Option " )
    
    # Create Dropdown menu
    Column_index =0
    drop_ports = OptionMenu( root , clicked_Ports[NumberOfConfiguredPorts] , *Port_Names )
    drop_ports.grid(row=Row_index, column=Column_index)  

    # Create Dropdown menu
    Column_index += 5
    drop_pins = OptionMenu( root , clicked_Pins[NumberOfConfiguredPorts] , *Pin_Numbers )
    drop_pins.grid(row=Row_index, column=Column_index) 

    # Create Dropdown menu
    Column_index += 5
    drop_pins_Options = OptionMenu( root , clicked_Pin_Options[NumberOfConfiguredPorts] , *Pin_Options )
    drop_pins_Options.grid(row=Row_index, column=Column_index) 
    NumberOfConfiguredPorts += 1

def main():
    global LoadedPortsIndication
    # parse input files
    for i in range (32):
        clicked_Ports.append(i)
        clicked_Pins.append(i)
        clicked_Pin_Options.append(i)
        loaded_Ports.append(i)
        loaded_Pins.append(i)
        loaded_Pin_Options.append(i)
        loaded2_Ports.append(i)
        loaded2_Pins.append(i)
        loaded2_Pin_Options.append(i)
    input_jmls_Parser() 
    # Create button, it will change label text
    button_add = Button( root , text = "Click to add Configuration" , command = show ).place(x=700, y= 0) 
    button_Save = Button( root , text = "Save configuration" , command = Save  ).place(x=720, y= 30) 
    button_Generate = Button( root , text = "Generate" , command = Generate  ).place(x=750, y= 60) 
    button_Generate = Button( root , text = "Load" , command = load  ).place(x=765, y= 90)
    if( LoadedPortsIndication == 1):
        # Create button, it will change label text
        load()
        LoadedPortsIndication = 0
    # Execute tkinter
    root.mainloop()

    
if __name__ == "__main__":
    main()
