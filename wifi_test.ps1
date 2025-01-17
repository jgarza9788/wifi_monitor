
$thisDate = Get-Date

# # test Error 404
# netsh wlan connect name="Error 404"
# Start-Sleep -Seconds 10.0
# .\pinger.ps1
# Start-Sleep -Seconds 5.0
# Write-Host ""

# git add *
# git commit -m "wifi-test $($thisDate)"
# git push
# Write-Host ""

# # test Error 404_EXT
# netsh wlan connect name="Error 404_EXT"
# Start-Sleep -Seconds 10.0
# .\pinger.ps1
# Start-Sleep -Seconds 5.0
# Write-Host ""

# git add *
# git commit -m "wifi-test $($thisDate)"
# git push
# Write-Host ""

# # test Error 404 NH
# netsh wlan connect name="Error 404 NH"
# Start-Sleep -Seconds 10.0
# .\pinger.ps1
# Start-Sleep -Seconds 5.0
# Write-Host ""

# git add *
# git commit -m "wifi-test $($thisDate)"
# git push
# Write-Host ""

# generate report
jupyter nbconvert --to notebook --execute reports.ipynb

git add *
git commit -m "wifi-test $($thisDate)"
git push
Write-Host ""