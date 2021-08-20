#!/bin/bash

# Author: Tobias Weisskopf
# Date: 2021-08-20
# Description: Tool to gather Forensic Evidence from MacOS


logfile=$1
filename='triage_dump.txt'

mkdir SystemInformation
mkdir InstalledApplications
mkdir Logs

# Getting System Information
echo "Starting Acquisition"

echo "\t Getting System Information"

# System Information
plutil -p /System/Library/CoreServices/SystemVersion.plist
cp /System/Library/CoreServices/SystemVersion.plist SystemInformation/

# -------------- Installed Applications -------------------------
# Installed Applications
# Update History
# Appstore Settings (Global and User)

echo "Installed Applications"

# Installation History
plutil -p /Library/Receipts/InstallHistory.plist
cp /Library/Receipts/InstallHistory.plist InstalledApplications/

# Printing File System Entries from /var/db/receipts
ls /var/db/receipts

# Software Update Information

# Software Update List
plutil -p /Library/Preferences/com.apple.SoftwareUpdate.plist
cp /Library/Preferences/com.apple.SoftwareUpdate.plist InstalledApplications/

# User specific Updatejournal
plutil -p '~/Library/Application Support/App Store/updatejournal.plist'
cp '~/Library/Application Support/App Store/updatejournal.plist' InstalledApplications/

# Global AppStore Settings
plutil -p /Library/Preferences/com.apple.commerce.plist
cp /Library/Preferences/com.apple.commerce.plist InstalledApplications/

# User Specific AppStore Settings
plutil -p '~/Library/Preferences/com.apple.commerce.plist'
cp '~/Library/Preferences/com.apple.commerce.plist' InstalledApplications/

# --------------- LOG FILES -------------------------

echo "Copying Log Files"

# Log File
cp /var/log/install.log Logs/


echo "----------------------------"
echo "End of Gathering Information"
