
$thisDate = Get-Date

# Start-Process ms-settings:network-wifi
# netsh wlan show networks mode=bssid
netsh wlan show networks mode=bssid


function Connect-ToWiFi {
    param (
        [string]$wifiName,
        [int]$retryInterval = 10,
        [int]$maxTries = 5
    )

    $attempts = 0

    while ($attempts -lt $maxTries) {
        Write-Host "Connecting to $wifiName..."
        
        $output = netsh wlan connect name=$wifiName
        if ($output -notmatch "is not available to connect") {
            Write-Host "✅ $wifiName" -ForegroundColor Green
            return $true
        }

        $attempts++
        Write-Host "🔁 Retry $retryInterval seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds $retryInterval
    }

    Write-Host "❌ $wifiName" -ForegroundColor Red
    return $false
}


function DoGit()
{
    git add *
    git commit -m "wifi-test $($thisDate)"
    git push
    Write-Host "✅ pushed"
}


Connect-ToWiFi -wifiName "Error 404"
Connect-ToWiFi -wifiName "Error 404 NH"
Connect-ToWiFi -wifiName "Error 404_EXT"



# test Error 404
Connect-ToWiFi -wifiName "Error 404"
Start-Sleep -Seconds 10.0
.\pinger.ps1
Write-Host ""
DoGit

# test Error 404 NH
Connect-ToWiFi -wifiName "Error 404 NH"
Start-Sleep -Seconds 10.0
.\pinger.ps1
Write-Host ""
DoGit

# test Error 404_EXT
Connect-ToWiFi -wifiName "Error 404_EXT"
Start-Sleep -Seconds 10.0
.\pinger.ps1
Write-Host ""
DoGit

# generate report
jupyter nbconvert --to python --execute reports.ipynb
DoGit