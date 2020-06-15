# SmartCitiesProject
Practical Assignment for Smart Cities and IoT Lecture of University of Stuttgart

Then, navigate to the respective folder of the component you'd like to run. There is a specific folder containing a MQTTClient for each of the component of System. Each of them is described below.

###### Sensor
The folder `Sensor` contains the code for the Raspberry responsible for controlling the sensors. If that's your case, execute `python3 SensorRaspberryMain.py` in the `Sensor` directory.

###### Action
The folder `Action` contains the code for the Raspberry responsible for controlling the actuators. If that's your case, execute `python3 ActionRaspberryMain.py` in the `Action` directory.

###### Server
The folder `Server` contains the code for the Server of the system. It is responsible for receiving the first raspberry messages and sending them to the second. If that's the case, execute `python3 ServerMain.py` in the `Server` directory.

When executing for the first time, before running the code execute the `install.sh` script in the respective forder like the following.

- sh ./install.sh
