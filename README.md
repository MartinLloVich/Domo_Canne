# 🔧 **DomoCanne: Domotics System for Pet-Friendly Homes**

## 📋 **Project Description**
This repository contains the code and documentation of the project developed for the course **"Domotics. Intelligent Environments"** of the Master’s in Automation and Robotics at UPM.  

The system automates a home with pets, integrating features such as:  

- 🐕 **Automatic door opening** to the garden using a presence sensor  
- 🍖 **Automatic feeder** with email alerts when food is low  
- 🌡️ **Climate control** with ventilation and emergency mode in case of fire  
- 📱 **Mobile app** for monitoring and remote control  

---

## 🗂️ **Repository Structure**
```text
📁 DomoCanne/
│
├── 📁 hardware/                 # Hardware diagrams and connections
├── 📁 software/                 # Python and Arduino code
│   ├── dar_comida.py            # Automatic feeder control
│   ├── alerta_comida.py         # Low food detection
│   ├── email_server.py          # Sending email alerts
│   ├── servo_control.py         # Servo control for the door
│   ├── domo_canne_main.py       # Main program
│   └── launcher.sh              # System startup script
├── 📁 docs/                     # Documentation and presentation
├── 📁 maqueta/                  # Model photos and design
│
└── 📄 README.md                 # This file
```


## 🛠️ Technologies and Components

| **Component** | **Function** |
|---------------|--------------|
| Raspberry Pi 4 | Central control unit |
| Arduino UNO | Data acquisition and actuators |
| HC-SR04 Sensor | Presence detection |
| SG90-9g Servo | Door opening |
| DHT11 Sensor | Temperature and humidity |
| DC Motor 130 + Fan | Climate control |
| SSLDR67 Light Sensor | Food detection |
| 28BYJ-48 Stepper Motor | Automatic feeder |

## 🧠 Implemented Features

### ✅ Automations

- **Automatic Door:** Opens when presence is detected by the ultrasonic sensor.  
- **Automatic Feeder:** Dispenses food and sends an email alert if food is low.  
- **Climate Control:** Activates ventilation if temperature exceeds safe thresholds.  
- **Emergency Mode:** In case of fire, doors open and forced ventilation is activated.  

### 📱 Mobile App

- Remote control of all functionalities.  
- Real-time temperature and humidity monitoring.  
- Enable/disable safe mode.  

### 📧 Communications

- Email alerts (SMTP) for critical events.  
- MQTT protocol for device communication.  
- REST API for mobile app integration.  

## 🔌 Connections and Protocols

### MQTT Topics Used

- `DomoCanne/safe_mode`  
- `DomoCanne/temperature`  
- `DomoCanne/humidity`  
- `DomoCanne/feed_food`  
- `DomoCanne/food_sensor`  

### Serial Communication

- UART between Raspberry Pi and Arduino for sensor reading.  

## 📊 Connection Diagram

The system includes:  

- **Raspberry Pi** as the central brain running Python.  
- **Arduino** for reading analog/digital sensors.  
- Communication via **UART serial**.  
- **Motor and actuator drivers.**  
- **Power and protection circuitry.**  

## 🎓 Academic Context

Project developed by **David Laborda Izquierdo** and **Martín Loring Bueno** for the course *Domotics. Intelligent Environments* of the **Master’s in Automation and Robotics** at the **Polytechnic University of Madrid**.  

## 📧 Contact
 
✉️ martin.loringbueno@hotmail.com  
🔗 [LinkedIn](www.linkedin.com/in/martin-loring-bueno-830886233)
