# IVT-Sensor Config
This script allows some basic configuration for the IVT-S Sensors. Please read the Reame carefully before using the script.
For some more informatin about the Messages in general: ![IVT.md](IVT.md)

## Requirements
- Peak Can Hardware (not tested with anything else)
- Peak Can Driver (not tested with anything else)
- Python 3
    - tkinter, python can
    - Simply run *pip install -r requirements.txt*
- (optional) BusMaster
- (optional) custom DBC File

## Staring the script
- Make sure Requrements are installed and Peak Can is *connected* and not in use by any other software
- Once the Script started, Peak Can may be used by other software simultaneously (e.g. BusMaster) to monitor everything.
- Alternatively, a precompiled .exe exists in src/dist...
  - To recompile, run *pyinstaller IVTConfig.spec* within the src folder.

## Confiure Can IDs 
- This Script only changes the first Bit of the CAN ID as per user Input. Therefore only 8 different Sensors may be configured this way. Feel free to change, it just fits my requrements like this.
- In the UI, enter "New Custom IDentifier", current Command Id, Serial Number and select the Messages that are to be configured.
- Run the Config procedure:

    1. Send Stop
    2. Send Config (note: multiple things may be configured at this point)
    3. Send Store

## Confiure Trigger Mode and Measurement Cycle 
- Select the Trigger Mode
- Select the Measurement Cycle (0 is ignored)

    1. Send Stop
    2. Send Config (note: multiple things may be configured at this point)
    3. Send Store
    4. Send Run 

## Confiure Command ID
- Enter current Command ID
- Enter new Command ID

    1. Send Stop
    2. Send Config (note: multiple things may be configured at this point) (note: The current Command ID changes automatically)
    3. Send Store
    4. Send Run 

- How to get the current command ID
    - On Restart, the Sensors sends a Message containing it's command ID in DB 1&2. 
        - If multiple Sensors share the same response ID, make sure only one Sensor is connected at that time.
        - For more information, read the IVT-S How To's document
     
