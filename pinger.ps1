# Get the current SSID
$SSID = (netsh wlan show interfaces | Select-String -Pattern '^ *SSID' | ForEach-Object { ($_ -split ': ')[1].Trim() })
Write-Host "SSID: $SSID"

# Get current date and time in two formats
$dateTimeDefault = Get-Date
Write-Host "Default DateTime: $dateTimeDefault"

$dateTimeCustom = Get-Date -Format "yyyyMMddHHmm"
Write-Host "Custom DateTime: $dateTimeCustom"

$signalStrength = (netsh wlan show interfaces) -Match '^\s+Signal' -Replace '^\s+Signal\s+:\s+',''    

# Replace spaces in SSID to create a file-friendly name
$nameSSID = $SSID -replace " ", ""

# Construct the file name
$folder = "reports"

if (-not (Test-Path -Path $folder)) {
    New-Item -ItemType Directory -Path $folder 
    Write-Host "Created folder: $folder"
} else {
    Write-Host "Folder already exists: $folder"
}

$File = "$($folder)\$($nameSSID)_$($dateTimeCustom).txt"
Write-Host "File Name: $File"

# Write SSID and datetime to the file
"SSID: $SSID" | Out-File -Append -FilePath $File
"Datetime: $dateTimeDefault" | Out-File -Append -FilePath $File
"Datetime_alt: $dateTimeCustom" | Out-File -Append -FilePath $File
"Signal_Strength: $signalStrength" | Out-File -Append -FilePath $File

# Append ping results to the file
ping google.com -n 100 | Out-File -Append -FilePath $File

# Confirm file creation
Write-Host "File created at: $File"
