#!/bin/bash

# Get the current SSID
SSID=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d':' -f2)
echo "SSID: $SSID"

# Get current date and time in two formats
dateTimeDefault=$(date)
echo "Default DateTime: $dateTimeDefault"

dateTimeCustom=$(date +"%Y%m%d%H%M")
echo "Custom DateTime: $dateTimeCustom"

# Get signal strength
signalStrength=$(nmcli -t -f IN-USE,SIGNAL dev wifi | grep '^*' | cut -d':' -f2)

# Replace spaces in SSID to create a file-friendly name
nameSSID=$(echo "$SSID" | tr -d ' ')

# Construct the file name
folder="reports"

if [[ ! -d "$folder" ]]; then
    mkdir "$folder"
    echo "Created folder: $folder"
else
    echo "Folder already exists: $folder"
fi

file="$folder/${nameSSID}_${dateTimeCustom}.txt"
echo "File Name: $file"

# Write SSID and datetime to the file
{
    echo "SSID: $SSID"
    echo "Datetime: $dateTimeDefault"
    echo "Datetime_alt: $dateTimeCustom"
    echo "Signal_Strength: $signalStrength"
} >> "$file"

# Append ping results to the file
ping -c 100 google.com >> "$file"

# Confirm file creation
echo "File created at: $file"
