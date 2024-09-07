
# SmartBins_RPi_Blynk (only Driver code)

### Overview
This repository showcases my **Smart Bins** project developed during my internship. The project integrates **Raspberry Pi**, **Blynk**, and **machine learning** to automate waste sorting and monitoring. Ultrasonic sensors monitor bin capacity, and servos automatically open the correct bin based on the type of waste detected. The Blynk app is used for real-time monitoring and control.

### Technologies Used
- **Raspberry Pi (RPi)** for hardware control
- **Blynk** for IoT platform and mobile app integration
- **Ultrasonic Sensors** to check bin levels
- **Servos** for automatic bin opening
- **Machine Learning** for waste type detection (via camera)
- **Python** (RPi GPIO, Blynk, and ML libraries)

### Project Features
1. **Smart Bin Automation**: Automatically opens the bin based on the type of waste detected using a machine learning model.
2. **Real-Time Monitoring**: Bin levels are monitored via ultrasonic sensors and displayed on the Blynk app.
3. **Remote Control**: Bins can be manually controlled using the Blynk app if needed.
4. **Machine Learning Integration**: The system predicts the waste type using camera input and opens the corresponding bin.

---

## How It Works

### Hardware Setup
- **Ultrasonic Sensors**: Measure the level of waste in the bins to determine if they are full.
- **Servo Motors**: Control the opening of bins automatically when waste is detected.
- **Camera**: Captures an image of the waste, which is processed by a machine learning model to classify the waste type.

### Software Workflow
1. **Sensor Check**: Ultrasonic sensors continuously monitor the fill level of each bin.
2. **Waste Detection**: The camera captures an image of the waste, which is then processed by the machine learning model to classify it.
3. **Bin Control**: Based on the waste type, the corresponding bin’s servo opens, allowing the user to dispose of the waste.
4. **Blynk Integration**: Real-time updates on bin levels are sent to the Blynk app, allowing users to monitor and control the system remotely.

---

## Files

1. [**Sensor and Actuator Test Code**](./test_code)
   - This script tests the functionality of the ultrasonic sensors and servos to ensure they work as expected.
   - Useful for debugging and hardware calibration.

2. [**Smart Bin Driver Code**](./driver_code)
   - The main code for the smart bin system.
   - Integrates the ultrasonic sensors, servos, and machine learning model for waste classification and automated bin control.

---

## Getting Started

### Prerequisites
- Raspberry Pi with internet connectivity.
- Blynk app (iOS/Android) for remote control.
- Python libraries: `RPi.GPIO`, `blynklib`, `opencv`, `tensorflow` (or other ML libraries).

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/SmartBins_RPi_Blynk.git
    cd SmartBins_RPi_Blynk
    ```

2. Install the necessary Python libraries:
    ```bash
    pip install RPi.GPIO blynklib opencv-python tensorflow
    ```

3. Set up your Blynk account, and get your unique authentication token from the app.

---

## Running the Project

### Testing Sensors and Actuators:
1. Navigate to the test script:
   ```bash
   cd test_code
   python test_sensors_actuators.py
   ```

2. Ensure that all sensors and servos are functioning correctly.

### Running the Smart Bin System:
1. Navigate to the smart bin driver code:
   ```bash
   cd driver_code
   python smart_bins.py
   ```

2. The system will begin monitoring bin levels, classify waste, and automatically open the correct bin.

---

## Future Enhancements
- Improve machine learning waste classification accuracy.
- Add a notification system to alert when bins are full.
- Incorporate solar energy or low-power modes for sustainable operation.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements or suggestions.

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

This `README.md` outlines your smart bins project, emphasizing automation, waste classification, and IoT control. Let me know if you want further tweaks!
