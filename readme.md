# Mac Forensics

Author: Tobias Weisskopf

Date: 2021-08-20

Description: Python Application to get Forensic Artifacts from macOS. Information on Forensic Artifacts used from [1] (Brandt M., 2017)

License: MIT

Status: Active

---

## Implemented Features

The following table track the implemented artifacts so far.

Artifacts|Status
---|---
Logs|Testing
InstalledApplications|Testing
NetworkSettings|Testing
Printers|Testing
SystemInformation|Testing
UserAccounts|In Progress
Keychains|Not Started
Firewall|Not Started
Launch Agents|Not Started
Launch Daemons|Not Started
Freigaben|Not Started
Keychains|Not Started
User Domain|Not Started

---

## Installation Instructions

1. Clone Repository to your local machine
2. Copy the repository to a USB Stick
3. Connect USB Stick to the target device and,
4. Open a terminal at the location of the script `/Volumes/<USBSTICK>`
5. Run nidaba.py with sudo rights `sudo nidaba.py`

---

## Contributions

Contributors are welcome, please contact me if you like to help in the development.

---

## References

[1] Brandt, M. (2017). Mac OS Hacking: Professionelle Werkzeuge und Methoden zur forensischen Analyse des Apple-Betriebssystems. Haar: Franzis Verlag.
