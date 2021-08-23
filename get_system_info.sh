#!/bin/bash

# Author: Tobias Weisskopf
# Date: 2021-08-20
# Description: Tool to gather Forensic Evidence from MacOS

# TODO! Ask user to enter a case number, a analyst etc.
#read "Please enter a case number"
filename=0000_test_file.txt
locations=locations.conf

# Check if Folders already exist
directories=("SystemInformation" "Logs" "InstalledApplications")

for DIRECTORY in "${directories[@]}"
do
    if [ -d "$DIRECTORY"]; then
        rm -rf $DIRECTORY
    else
        mkdir $DIRECTORY
    fi
done

# FEATURE add data to configuration file.
# Loading Data from the configuration file
while read -r plist_path; do 
    get_plist_artifact $plist_path
done < $locations

# Function to get all PLIST Artifacts
get_plist_artifact() {
    plutil -p $plist_path >> $filename
    cp -p $plist_path $artifact_category
}

# Copying Logfiles
get_logfiles(){
    cp -p $logfile_path Logs/
}


echo "Starting Acquisition by $USER on $HOSTNAME"

# Getting System Information

echo "Getting System Information"

# System Information
plutil -p /System/Library/CoreServices/SystemVersion.plist
cp -p /System/Library/CoreServices/SystemVersion.plist SystemInformation/

# Time of installation
cp -p '/private/var/db/.Apple*' SystemInformation/

# Get TimeZone information
plutil -p /Library/Preferences/.GlobalPreferences.plist
ls -l /etc/localtime


# -------------- Installed Applications -------------------------
# Installed Applications
# Update History
# Appstore Settings (Global and User)

echo "Installed Applications"

# Installation History
plutil -p /Library/Receipts/InstallHistory.plist
cp -p /Library/Receipts/InstallHistory.plist InstalledApplications/

# Printing File System Entries from /var/db/receipts
ls /var/db/receipts

# Software Update Information

# Software Update List
plutil -p /Library/Preferences/com.apple.SoftwareUpdate.plist
cp -p /Library/Preferences/com.apple.SoftwareUpdate.plist InstalledApplications/

# User specific Updatejournal
plutil -p '~/Library/Application Support/App Store/updatejournal.plist'
cp -p '~/Library/Application Support/App Store/updatejournal.plist' InstalledApplications/

# Global AppStore Settings
plutil -p /Library/Preferences/com.apple.commerce.plist
cp -p /Library/Preferences/com.apple.commerce.plist InstalledApplications/

# User Specific AppStore Settings
plutil -p '~/Library/Preferences/com.apple.commerce.plist'
cp -p '~/Library/Preferences/com.apple.commerce.plist' InstalledApplications/

# --------------- LOG FILES -------------------------

echo "Copying Log Files"

# Log File
cp -p /var/log/install.log Logs/


echo "----------------------------"
echo "End of Gathering Information"
