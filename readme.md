# Mac Forensics

Author: Tobias Weisskopf

Date: 2021-08-20

Description: Python Application to get Forensic Artifacts from macOS. Information on Forensic Artifacts used from [1] (Brandt M., 2017)
Relies on python standard library, so no external libraries are required.

License: MIT

Status: Active

---

## Disclaimer

Use @ your own risk, since this application is still in ALPHA no extensive testing has been done (yet). If you want to help see Contributions section.

---

## Implemented Features

The following table keeps track of the artifacts covered:

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

See locations.csv for detailed list of artifacts.

---

## Installation Instructions

1. Clone Repository to your local machine
2. Copy the repository to a USB Stick
3. Connect USB Stick to the target device and,
4. Open a terminal at the location of the script `/Volumes/<USBSTICK>`
5. Run nidaba.py with sudo rights `sudo python3 nidaba.py`

---

## Contributions

Contributors are welcome, please contact me if you like to help in the development. Either on GitHub or via my Twitter handle @_APTwi

---

## References

[1] Brandt, M. (2017). Mac OS Hacking: Professionelle Werkzeuge und Methoden zur forensischen Analyse des Apple-Betriebssystems. Haar: Franzis Verlag.
