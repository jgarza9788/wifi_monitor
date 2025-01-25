#!/bin/bash

thisDate=$(date)

# Test Error 404
nmcli dev wifi connect "Error 404"
sleep 15
bash ./pinger.sh
echo ""

git add *
git commit -m "wifi-test $thisDate"
git push
echo ""

# Test Error 404_EXT
nmcli dev wifi connect "Error 404_EXT"
sleep 15
bash ./pinger.sh
echo ""

git add *
git commit -m "wifi-test $thisDate"
git push
echo ""

# Test Error 404 NH
nmcli dev wifi connect "Error 404 NH"
sleep 15
bash ./pinger.sh
echo ""

git add *
git commit -m "wifi-test $thisDate"
git push
echo ""

# Generate report
jupyter nbconvert --to python --execute reports.ipynb

git add *
git commit -m "wifi-test $thisDate"
git push
echo ""
