# netsh wlan show interfaces
# netsh interface set interface name="Wi-Fi" admin=enable
# Get-NetAdapter | Where-Object { $_.Status -eq 'Up' }
# net stop WlanSvc
# net start WlanSvc
# Get-NetAdapter -InterfaceDescription "*Wi-Fi*" | Get-NetConnectionProfile

netsh wlan show networks mode=bssid
