import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import can


sensor_messages = ["All","IVT_Msg_Result_I", "IVT_Msg_Result_U1", "IVT_Msg_Result_U2", "IVT_Msg_Result_U3", "IVT_Msg_Result_T", "IVT_Msg_Result_W", "IVT_Msg_Result_As", "IVT_Msg_Result_Wh", "IVT_Msg_Response"]#, "IVT_Msg_Command"]
canid_config_id_values = [0, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x1F]# 0x1D]  #These Values are needed to tell the sensor what ID is to be changed
result_config_id_values = [0, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27]  #These Values are needed to tell the sensor what Response is to be changed
new_can_id = [0, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x11]  #This is the default 2nd bit of the Id, this script only changes the first as per user input
trigger_mode = ["disabled", "triggered", "cyclic running (default)"]
trigger_mode_config =  [0x0, 0x1, 0x2]




class CANApp:

    def __init__(idconfig, root):
        
        idconfig.root = root
        idconfig.root.title("IVT-S Sensor ID Configurator")
        idconfig.root.minsize(920, 350)  # Set the minimum size of the window in pixels

        # Configure grid layout
        idconfig.root.columnconfigure(0, weight=1)
        idconfig.root.columnconfigure(1, weight=1)
        idconfig.root.columnconfigure(2, weight=1)
        idconfig.root.columnconfigure(3, weight=1)
        idconfig.root.rowconfigure(0, weight=1)
        idconfig.root.rowconfigure(1, weight=1)
        idconfig.root.rowconfigure(2, weight=1)
        idconfig.root.rowconfigure(3, weight=1)
        idconfig.root.rowconfigure(4, weight=10)
        idconfig.root.rowconfigure(5, weight=1)
        idconfig.root.rowconfigure(6, weight=1)
        idconfig.root.rowconfigure(7, weight=1)
        idconfig.root.rowconfigure(8, weight=1)
        idconfig.root.rowconfigure(9, weight=1)
        idconfig.root.rowconfigure(10, weight=1)
        idconfig.root.rowconfigure(11, weight=1)

        # Row one text
        idconfig.text = tk.Label(root, text = "Enter Values in Decimal, default Commamnd ID is 1041. With Custom DBC, use 1024 (0x400). Read the documentation before use!")
        idconfig.text.grid(row=0,  columnspan=4, sticky='ew', padx=30, pady=5)

        # Column 0: Measurement Cycle
        idconfig.cycle_label = tk.Label(root, text="Measurement Cycle (ms)")
        idconfig.cycle_label.grid(row=6, column=0, sticky='sew', padx=10, pady=5)
        idconfig.cycle_entry = tk.Entry(root)
        idconfig.cycle_entry.grid(row=7, column=0, sticky='new', padx=10, pady=5)

        # Column 0: New Command ID
        idconfig.new_cmd_ID = tk.Label(root, text="Enter custom Command ID")
        idconfig.new_cmd_ID.grid(row=9, column=0, sticky='sew', padx=10, pady=5)
        idconfig.new_cmd_ID = tk.Entry(root)
        idconfig.new_cmd_ID.grid(row=10, column=0, sticky='ew', padx=10, pady=5)

        # Culumn 1: Current Command ID
        idconfig.cmd_ID = tk.Label(root, text="Enter current Command ID")
        idconfig.cmd_ID.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        idconfig.cmd_ID = tk.Entry(root)
        idconfig.cmd_ID.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        # Column 2: Serial Number input
        idconfig.serial_label = tk.Label(root, text="Serial Number:")
        idconfig.serial_label.grid(row=1, column=2, sticky='ew', padx=10, pady=5)
        idconfig.serial_entry = tk.Entry(root)
        idconfig.serial_entry.grid(row=2, column=2, sticky='ew', padx=10, pady=5)

        # Column 0: Number input
        idconfig.number_label = tk.Label(root, text="New Custom Identifier (0-7):")
        idconfig.number_label.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        idconfig.number_entry = tk.Entry(root)
        idconfig.number_entry.grid(row=2, column=0, sticky='ew', padx=10, pady=5)


 	    # Column 3: Dropdown Message select
        idconfig.dropdown_label = tk.Label(root, text="Select wich messages are to be configured")
        idconfig.dropdown_label.grid(row=1, column=3, sticky='ew', padx=10, pady=5)
        idconfig.dropdown = ttk.Combobox(root, 	values = sensor_messages)
        idconfig.dropdown.grid(row=2, column=3, sticky='ew', padx=10, pady=5)

        # Column 1: Dropdown trigger Mode
        idconfig.trigger_label = tk.Label(root, text="Select the Trigger Mode")
        idconfig.trigger_label.grid(row=4, column=0, sticky='sew', padx=10, pady=5)
        idconfig.trigger = ttk.Combobox(root, 	values = trigger_mode)
        idconfig.trigger.grid(row=5, column=0, sticky='new', padx=10, pady=5)
  

    	# Send Stop button
        idconfig.sendStop_button = tk.Button(root, text="1) Send Stop", command=idconfig.stop_can_message)
        idconfig.sendStop_button.grid(row=3, column=1, padx=10, pady=10)

        # Send configure ID button 
        idconfig.sendConfigID_button = tk.Button(root, text="2) Send Config ID", command=idconfig.config_id_can_message)
        idconfig.sendConfigID_button.grid(row=3, column=0, padx=10, pady=10)
     
        # Send configure Trigger button 
        idconfig.sendConfigTrigger_button = tk.Button(root, text="2) Send Config Trigger", command=idconfig.config_response_can_message)
        idconfig.sendConfigTrigger_button.grid(row=8, column=0, padx=10, pady=10, sticky = 'new')
        
        # Store button
        idconfig.sendStore_button = tk.Button(root, text="3) Send Store", command=idconfig.store_can_message)
        idconfig.sendStore_button.grid(row=3, column=2, padx=10, pady=10)
        
        # Send run
        idconfig.sendRun_button = tk.Button(root, text="4) Send Run", command=idconfig.run_can_message)
        idconfig.sendRun_button.grid(row=3, column=3, padx=10, pady=10)

        # Send custom Command ID
        idconfig.sendcustom_button = tk.Button(root, text="2) Send custom Command ID", command=idconfig.command_id_can_message)
        idconfig.sendcustom_button.grid(row=11, column=0, padx=10, pady=10, sticky = 'new')

        # Help button
        idconfig.help_button = tk.Button(root, text="Help", command=idconfig.help)
        idconfig.help_button.grid(row=0, column=3, padx=10, pady=10, sticky = 'e')

        # Connect
        idconfig.connect = tk.Button(root, text="Connect", command = idconfig.initialize_can_interface)
        idconfig.connect.grid(row=0, column=0, padx=10, pady=10, sticky = 'w')

        # Terminal display 
        idconfig.terminal = scrolledtext.ScrolledText(root, state='disabled', height = 15)
        idconfig.terminal.grid(row=4, rowspan = 8, column=1, columnspan=3, sticky='nsew', padx=10, pady=10)
        idconfig.root.rowconfigure(3)

        # Disable all Buttons
        idconfig.disable_can_dependent_widgets()
        idconfig.initialize_can_interface()
        

#################################################################################
    def initialize_can_interface(idconfig):
        try:
            bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000) # Only tested on Windows
            #bus = can.Bus(interface='virtual', channel='virutal', bitrate=500000)# Virtual Bus Win, not tested
            #bus = can.interface.Bus(channel='vcan0', bustype='socketcan')# Virtual Bus Lin
            idconfig.bus = bus
            idconfig.enable_can_dependent_widgets()
            idconfig.log_message(f"{bus.channel_info} - Successfully Connected")
        except Exception  as e:
            messagebox.showerror("ERROR", "Could not initialize Can Hardware.")
            idconfig.log_message(f"Only Peak Can tesed, Hardware needs to be connected!\nError initializing CAN interface: {str(e)}")


    def config_id_can_message(idconfig):
        try:
            serial_number = int(idconfig.serial_entry.get())
            number = int(idconfig.number_entry.get())
            msg_dropdown_val = idconfig.dropdown.get()
            command_id = int(idconfig.cmd_ID.get())
            if not (0 <= number <= 7):
                raise ValueError("Number must be between 0 and 7")
            if msg_dropdown_val == '':
                raise ValueError("Please Select a Message")
            if command_id == 1041 and number == 4:
                raise ValueError("With Command ID 1041 (0x411), 4 is not allowed as ID config, since Command ID and Response ID would be the same then.")
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")
            return




        # Get the Info from the User Inputs and write can Message(s)
        selection_index = sensor_messages.index(msg_dropdown_val)      
        if msg_dropdown_val == "All": # Create and send all messages
            idconfig.log_message(f"\nAll Signals will be updated")
            for sel in sensor_messages:
                selection_index = sensor_messages.index(sel)
                selection = new_can_id[selection_index]
                if selection != 0: # "All" ausschließen
                    # Convert numbers to bytes
                    serial_number_bytes = serial_number.to_bytes(4, 'big')
                    number_bytes = number.to_bytes(1, 'big')
                    # Pack Can message
                    data = [canid_config_id_values[selection_index], number_bytes[0], selection, serial_number_bytes[0], serial_number_bytes[1], serial_number_bytes[2], serial_number_bytes[3]]
                    # Create CAN message
                    msg = can.Message(arbitration_id=command_id, data=data, is_extended_id=False)
                    idconfig.log_message(f"\n{sensor_messages[selection_index]} will be updated")
                    # Send
                    idconfig.can_message(msg)

        else: #Create and send specific Message
            selection = new_can_id[selection_index]
            idconfig.log_message(f"\n{sensor_messages[selection_index]} will be updated")
            # Convert numbers to bytes
            serial_number_bytes = serial_number.to_bytes(4, 'big')
            number_bytes = number.to_bytes(1, 'big')
            # Pack Can message
            data = [canid_config_id_values[selection_index], number_bytes[0], selection, serial_number_bytes[0], serial_number_bytes[1], serial_number_bytes[2], serial_number_bytes[3]]
            # Create CAN message
            msg = can.Message(arbitration_id=command_id, data=data, is_extended_id=False)
            # Send
            idconfig.can_message(msg)


#################################################################################
    def config_response_can_message(idconfig):
        try:
            serial_number = int(idconfig.serial_entry.get())
            cycle = int(idconfig.cycle_entry.get())
            msg_dropdown_val = idconfig.dropdown.get()
            trigger_dropdown_val = idconfig.trigger.get()
            command_id = int(idconfig.cmd_ID.get())
            if not (0 <= cycle <= 65534):
                raise ValueError("Number must be between 0 and 65534") 
            if msg_dropdown_val == '':
                raise ValueError("Please Select a Message")
            if trigger_dropdown_val == '':
                raise ValueError("Please Select a Trigger Mode")
            if msg_dropdown_val == "IVT_Msg_Response":
                raise ValueError("IVT_Msg_Response cannot be configured this way")
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")
            return


        # Get the Info from the User Inputs and write can Message(s)
        
        trigger_index = trigger_mode.index(trigger_dropdown_val) 
        selection = trigger_mode_config[trigger_index] # select the mode based on user Input   
        if msg_dropdown_val == "All": # Create and send all messages  
            for sel in sensor_messages:# Iterate trough every message
                if sel == "IVT_Msg_Response": #If this is reached, skip
                    return
                msg_index = sensor_messages.index(sel)
                message = result_config_id_values[msg_index]
                if message != 0: # "All" ausschließen
                    # Convert numbers to bytes
                    serial_number_bytes = serial_number.to_bytes(4, 'big')
                    number_bytes = cycle.to_bytes(2, 'big')
                    # Pack Can message
                    data = [result_config_id_values[msg_index], selection, number_bytes[0],number_bytes[1], serial_number_bytes[0], serial_number_bytes[1], serial_number_bytes[2], serial_number_bytes[3]]
                    # Create CAN message
                    msg = can.Message(arbitration_id=command_id, data=data, is_extended_id=False)
                    idconfig.log_message(f"\n{sensor_messages[msg_index]} will be updated")
                    # Send
                    idconfig.can_message(msg)

        else:
            msg_index = sensor_messages.index(msg_dropdown_val)
            idconfig.log_message(f"\n{sensor_messages[msg_index]} will be updated to  {trigger_dropdown_val}")
            # Convert numbers to bytes
            serial_number_bytes = serial_number.to_bytes(4, 'big')
            number_bytes = cycle.to_bytes(2, 'big')
            # Pack Can message
            data = [result_config_id_values[msg_index], selection, number_bytes[0],number_bytes[1], serial_number_bytes[0], serial_number_bytes[1], serial_number_bytes[2], serial_number_bytes[3]]
            # Create CAN message
            msg = can.Message(arbitration_id=command_id, data=data, is_extended_id=False)
            # Send
            idconfig.can_message(msg)
        
#################################################################################
    def store_can_message(idconfig):
        try:
            command_id = int(idconfig.cmd_ID.get())
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")
            return
        msg = can.Message(arbitration_id=command_id, data=[0x32, 0, 0], is_extended_id=False)
        idconfig.log_message(f"\nSending Store.")
        #idconfig.log_message(f"Can Message: {msg}")
        idconfig.can_message(msg)
        
#################################################################################
    def stop_can_message(idconfig):
        try:
            command_id = int(idconfig.cmd_ID.get())
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")
            return
        msg = can.Message(arbitration_id=command_id, data=[0x34, 0, 0x01], is_extended_id=False)
        idconfig.log_message(f"\nSending Stop.")
        #idconfig.log_message(f"Can Message: {msg}")
        idconfig.can_message(msg)

#################################################################################
    def run_can_message(idconfig):
        try:
            command_id = int(idconfig.cmd_ID.get())
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")
            return
        msg = can.Message(arbitration_id=command_id, data=[0x34, 0x01, 0x01], is_extended_id=False)
        idconfig.log_message(f"\nSending Run.")
       ##idconfig.log_message(f"Can Message: {msg}")
        idconfig.can_message(msg)
        
#################################################################################
    def log_message(idconfig, message):
        idconfig.terminal.config(state='normal')
        idconfig.terminal.insert(tk.END, message + "\n")
        idconfig.terminal.yview(tk.END)  # Scroll to the end
        idconfig.terminal.config(state='disabled')

#################################################################################
    def can_message(idconfig, message):
        try:
            idconfig.bus.send(message)
            idconfig.log_message(f"Message sent: {message}")
        except can.CanError as e:
            idconfig.log_message(f"CAN Error: {str(e)}")

#################################################################################
    def command_id_can_message(idconfig):
        try:
            current_command_id = int(idconfig.cmd_ID.get())
            serial_number = int(idconfig.serial_entry.get())
            new_command_id = int(idconfig.new_cmd_ID.get())
        except ValueError as e:
            idconfig.log_message(f"Invalid input: {str(e)}")

        idconfig.cmd_ID.delete(0, tk.END)
        idconfig.cmd_ID.insert(0, new_command_id)
        serial_number_bytes = serial_number.to_bytes(4, 'big')
        new_command_id_bytes = new_command_id.to_bytes(2, 'big')
        # Pack Can message
        data = [0x1D, new_command_id_bytes[0],new_command_id_bytes[1], serial_number_bytes[0], serial_number_bytes[1], serial_number_bytes[2], serial_number_bytes[3]]
        # Create CAN message
        msg = can.Message(arbitration_id=current_command_id, data=data, is_extended_id=False)
        # Send
        idconfig.can_message(msg)

    def disable_can_dependent_widgets(idconfig):
        # Disable all widgets that require CAN communication
        idconfig.sendStop_button.config(state=tk.DISABLED)
        idconfig.sendConfigID_button.config(state=tk.DISABLED)
        idconfig.sendConfigTrigger_button.config(state=tk.DISABLED)
        idconfig.sendStore_button.config(state=tk.DISABLED)
        idconfig.sendRun_button.config(state=tk.DISABLED)
        idconfig.sendcustom_button.config(state=tk.DISABLED)

    def enable_can_dependent_widgets(idconfig):
        # Enable all widgets once CAN is successfully initialized
        idconfig.sendStop_button.config(state=tk.NORMAL)
        idconfig.sendConfigID_button.config(state=tk.NORMAL)
        idconfig.sendConfigTrigger_button.config(state=tk.NORMAL)
        idconfig.sendStore_button.config(state=tk.NORMAL)
        idconfig.sendRun_button.config(state=tk.NORMAL)
        idconfig.sendcustom_button.config(state=tk.NORMAL)


#################################################################################
    def help(idconfig):
        idconfig.log_message("\n\nThis script helps to configure the IVT-S Sensors. These sensors are configured individually by their ID with the command message.\n")
        idconfig.log_message("To configure them, they have to be in stop mode 1) ander after configuration data needs to be stored 3). 4) is optional, restart should also work.")
        idconfig.log_message("\n1.: Result ID config \n  - This script allows to only configure the first bit of the ID. Therefore only 8 differnt sensors can be configured this way.")
        idconfig.log_message("\n2.: Response config \n  - Default mode is cyclic running, triggered not yet tested. More options available but not with this script.")
        idconfig.log_message("\n3.: Command ID Config \n - Enter the current Command ID and the new Command ID. ")
        idconfig.log_message("\n---------------------------------------------------------\n")
        idconfig.log_message("If your Command ID is not the default ID, here is how to find out your Command ID:")
        idconfig.log_message("\n    1. Connect only this Sensor properly to a Can Interface")
        idconfig.log_message("\n    2. Start the Interface, turn of the Sensor Power Supply")
        idconfig.log_message("\n    3. Turn on the Sensor Power Supply")
        idconfig.log_message("\n    4. On Restart, the Sensor sends its Command ID in DB 1&2 of the Response Message")
        idconfig.log_message("\nFor more details: IVT-S_HowTo_x.x.pdf")





if __name__ == "__main__":
    root = tk.Tk()
    app = CANApp(root)
    root.mainloop()

