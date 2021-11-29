# Supply-Chain-Management-Application
An application using python which sends live information to the Assembly Unit from the OEMs present under its supply chain. Also, a report will be generated at the end of the shift, and an Email must be sent automatically to the higher officials. This is to maintain a transparency throughout the supply chain so that the production could be economical and as efficient as possible.

#Working Principle:
The UI for the application is made using the tkinter package for python. Various modules are 
created to undergo individual tasks. Firstly, there is a timer module which countdowns the time 
in decrements and notifies when the Shift has ended. Once the Shift has ended, an automatic 
email is sent to respective authorities. The email consists of an excel file which contains the Shift 
details. The Automatic Mail sending module is made possible using the smtplib and email 
package available in python.
In case, the report of the shift is required in between the shift/before the shift ends, there is a 
Generate Report button. This button calls the module which is responsible for generating the 
report at the instance when it is clicked. The shift details are stored in an excel file using the 
pandas package. The excel file is named as the date and time at which the report was generated.
In order to get the live updates of the good and bad count from the Manufacturing Unit to the 
Assembly Unit, the values are published to a MQTT server online. In this case, we have used 
HiveMQ MQTT server. Using the paho-mqtt package in python, we would be able to call the 
necessary functions and publish the required values to the server. Simultaneously, the Assembly 
Unit would be receiving the values by subscribing to the respective topic in which it is getting 
published. Again, these values are displayed in the Assembly Unit application with tkinter being 
its base UI.
