
# Smart Public Lighting System with ESP32 and MQTT

This project implements a Smart Public Lighting System using an ESP32 microcontroller with integrated sensors (LDR for light measurement and PIR for motion detection). The system dynamically adjusts lighting based on environmental data, improving energy efficiency and enhancing safety in public areas.

The ESP32 collects and sends sensor data via the MQTT protocol to a cloud platform like FlowFuse (Node-RED), where the data is processed and visualized in real-time. This setup allows for remote monitoring and the visualization of metrics such as light intensity, the number of active LEDs, and motion detection.

**Benefits**

* *Energy Efficiency:* Public lighting is automatically adjusted to save energy, turning on only when needed.
* *Centralized Management:* Remote monitoring and real-time visual dashboards help in decision-making and system optimization.
* *Public Safety:* Enhanced lighting in public areas where motion is detected improves security.
* *Sustainability:* The system reduces energy consumption and operating costs, aligning with sustainable practices.

**Final Remarks**

This system can be expanded to integrate additional sensors and functionalities, such as air quality monitoring or security cameras, making it even more efficient for smart city management.

[![Apresentation]([https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/juliaprokofiev](https://www.youtube.com/watch?v=w2rhMHTx9N8))

## Features

**1. Intelligent Sensing**

LDR (Light Dependent Resistor): Measures ambient light levels to adjust LED brightness based on external conditions.
PIR (Passive Infrared Sensor): Detects motion and activates lighting in areas where it is needed.

**2. Automatic Lighting Control:** 
Adjusts the brightness of the LEDs based on the detected ambient light and motion.
Optimizes public lighting to save energy, turning on lights only when needed or when light levels are low.

**3. MQTT Integration**
The ESP32 sends sensor data (lux, interpolated lux, active LEDs) to an MQTT broker.
Data is published to the following topic:
pucpr/iot/ilum-motion-node: Sends information such as measured light intensity (lux), interpolated lux values, and the number of active LEDs.
Messages are published regularly or when changes occur, such as motion detection.

**4. Real-time Monitoring via FlowFuse (Node-RED)**
FlowFuse receives the data through MQTT and processes it to display in real-time on a dashboard.
Graphs and Indicators: The platform shows real-time graphs for ambient light, active LEDs, and motion detection, allowing city administrators to monitor and control the public lighting system remotely.
## Cloud Integration
**Data Flow**

*ESP32:*
Sensors for motion and light continuously monitor the environment.
The ESP32 processes the data and sends information such as lux, interpolated lux, and the number of active LEDs via MQTT to a cloud broker.

*MQTT Broker:*
Data is published to the MQTT broker (e.g., broker.mqttdashboard.com).
The broker distributes the data to clients, such as the FlowFuse system.

*FlowFuse (Node-RED):*
FlowFuse receives the MQTT messages published by the ESP32.
The data is processed and visualized in interactive real-time graphs on a dashboard.
Indicators such as the number of active LEDs and light intensity help monitor the system in real-time.


## 🛠 Setup
**Requirements**

*Hardware:*

* ESP32
* LDR Sensor
* PIR Sensor
* LEDs

*Software:*

* MicroPython v1.20 or higher for the ESP32
* MQTT Broker (e.g., broker.mqttdashboard.com)
* FlowFuse or Node-RED for data processing and visualization

**Setup Instructions**

*ESP32 Configuration:*

* Upload the provided code to the ESP32 to connect the sensors and send data via MQTT.

*FlowFuse Configuration:*

* Create flows to receive MQTT data and display it on the dashboard.
* Set up graphs to visualize lux values, active LEDs, and motion detection status.

![FlowFuse](https://github.com/user-attachments/assets/8a706ab9-f2c5-4684-9028-3a31316fd2f4)

*Monitoring:*

* Access the FlowFuse dashboard to monitor the system in real-time, view alerts, and adjust parameters as needed.

![dashboard - menor](https://github.com/user-attachments/assets/a3c3f2dd-0078-4b93-9311-02228cb479a4)


## 🔗 Links
[![Apresentation]([https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/juliaprokofiev](https://www.youtube.com/watch?v=w2rhMHTx9N8))
[![github](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/JuliaProkofiev)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/juliaprokofiev)


