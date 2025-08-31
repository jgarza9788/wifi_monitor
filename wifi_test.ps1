
$thisDate = Get-Date


# $SSIDs = @("Error 404", "Error 404 NH", "Error 404_EXT")
$SSIDs = @("Error 404", "Error 404 NH", "Error 404_EXT","Living Room Extension","Living Room Extension_6GHz")

$WIV = Start-Process ".\wifiinfoview\WifiInfoView.exe" -PassThru
Start-Sleep -Seconds 5

function Connect-ToWiFi {
    param (
        [string]$wifiName,
        [int]$retryInterval = 5,
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

foreach ($ssid in $SSIDs) {

    Write-Output "🟢 $ssid"
    Connect-ToWiFi -wifiName "$ssid"
    Start-Sleep -Seconds 10.0
    .\pinger.ps1
    Write-Host ""
    DoGit
    
}

# generate report
jupyter nbconvert --to python --execute reports.ipynb
DoGit

$WIV.kill()

