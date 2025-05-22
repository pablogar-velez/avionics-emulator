✈️ Avionics Systems Emulator
This project simulates communication between avionics systems such as the Flight Management System (FMS), Electronic Flight Instrument System (EFIS), Global Positioning System (GPS), and Autopilot, all interacting over a simulated ARINC-429 data bus. The tool includes a graphical user interface built with PyQt5, and features:

Real-time data bus monitoring

Translated and raw ARINC-429 message views

Module filtering

Fault injection (invalid data, delays, bit flips, dropped messages)

📦 Requirements
Install the necessary Python package:

pip install PyQt5
Python 3.7 or higher is recommended.

🚀 How to Run
Clone the repository:

git clone https://github.com/pablogar-velez/avionics-emulator.git
cd avionics-emulator
Run the main application:

python main.py
🖥️ Interface Overview
The GUI includes:

Module Filter: A dropdown to view messages from individual modules (GPS, FMS, EFIS, Autopilot, or Fault Injection), or all at once.

Translated Messages Panel: Human-readable interpretation of ARINC-429 messages.

Raw ARINC-429 Data Panel: Displays raw data frames.

Control Panel: Interface to trigger fault injections.

Aircraft-style Theme: Styled with aviation-inspired visuals and colors.

⚙️ Features
✅ ARINC-429 Message Simulation
Each module sends formatted messages containing:

Label (e.g. 101 for GPS)

SDI (Source/Destination Identifier)

Data field (varies by module)

SSM (Sign/Status Matrix)

✅ Message Translation
Messages are translated to human-readable formats using the message_translator.py logic.

✅ Filtering
You can filter messages by source module using the combo box:

ALL MODULES

GPS

FMS

EFIS

AUTOPILOT

FAULT INJECTION

✅ Fault Injection
Use the control panel to simulate errors:

Fault Type	Simulated Message
Inject Invalid Data	Label:999 SDI:0 Data:ERROR SSM:0
Inject Delay	Label:999 SDI:0 Data:DELAY SSM:0
Inject Bit Flip	Label:999 SDI:0 Data:BITFLIP SSM:0
Inject Drop Message	Label:999 SDI:0 Data:DROP SSM:0

Messages with label 999 or containing keywords like ERROR, FAULT, or INJECT are highlighted in red.

📁 Project Structure

avionics-emulator/
├── gui/
│   ├── main_window.py
│   ├── control_panel_widget.py
│   └── message_log_widget.py
├── messages/
│   ├── arinc429_message.py
│   └── message_translator.py
├── bus/
│   └── arinc_bus.py
├── main.py
└── README.md

🛠️ To Do / Ideas
Add logging to CSV or JSON

Support additional ARINC-429 labels

Add simulated error rates or continuous error modes

Include time stamps for each message