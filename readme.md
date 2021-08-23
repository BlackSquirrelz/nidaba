# Mac Forensics

Author: Tobias Weisskopf
Date: 2021-08-20

Bash Script to get Forensic Relevant Artifacts from MacOS. Information on Forensic Artifacts used from 
[1] (Brandt M., 2017)

Getting System Information and Installed Applications

[x] System Information
[x] Installed Applications


## Installation Instructions

1. Clone Repository to your local machine
2. Copy the repository to a USB Stick
3. Connect USB Stick to the target device and 
4. Open Terminal and change to the USB Stick
5. Give Executable rights to the application `chmod +x get_system_info.sh`
6. Execute the program with sudo `sudo ./get_system_info.sh`

NOTE: By default the tool will copy the artifacts with `cp -p` to preserve timestamps. The tool will create respective folders in the same folder
as the script location.

---

References

[1] Brandt, M. (2017). Mac OS Hacking: Professionelle Werkzeuge und Methoden zur forensischen Analyse des Apple-Betriebssystems. Haar: Franzis Verlag.
