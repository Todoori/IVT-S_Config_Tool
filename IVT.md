This Document gives a rough overview on how the IVT-S Sensors CAN messages look like.
A Can message contains a lot of different information, for us only the 11-bit Message Identifier (CAN-ID) and the 64-bit Can Message (Data) is of interest. 
Each message has it's unige CAN-ID.

The Datasheet displays the CAN IDs of the Sensor in Hex (0x...).
## Default messages
![](/misc/Bildschirmfoto_vom_2024-06-18_15-28-15.png)
- IVT_Msg_Command: This Message is the only message that is sent from the host to the Sensor. IN our case, this message can be the same for all the Sensors.
- Response Message: This Message is sent from the Sensor on different occaisons (Error, Startup, Change accepted...)
- Result Message: These are the messages of interest. If We use multiple Sensors, they need to be changed.

## Using the Script
### The Command Message
With the Command Message we can configure differnt things about the Sensor. This Script allows to configure the Sensors CAN-IDs and it's Can message frequency.
Since every Device on the CAN Bus get's the message and every Sensors has the same Command ID by default, the Command ID does also contain the serial number as another unique identifier. This does also need to be entered in the script.

The DBC File in this repository uses 0x400 as the command CAN-ID, if this DBC is used the command CAN-ID needs to be changed.

### The Result Messages
Since the Datasheet uses Hex CAN-IDs and I only needed a few Sensors to work, this Script only changes the Digit of the CAN-ID. With 11 bit this allows 8 differnt Sensors (Digit 0-7). The DBC File also works this way.
e.g.:
- Sensor1 :IVT_Msg_Result_I CAN-ID: 0x121
- Sensor0 :IVT_Msg_Result_I CAN-ID: 0x021
- Sensor4 :IVT_Msg_Result_I CAN-ID: 0x421
- ...

This is not a limitation in general, just a limitation of this script.
Might be changed in the future