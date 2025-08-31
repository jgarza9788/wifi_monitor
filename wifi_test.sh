networks=(
    "Error 404" 
    "Error 404_EXT" 
    "Error 404 NH" 
    "Living Room Extension" 
    "Living Room Extension_6GHz"
)

for net in "${networks[@]}"; do
    thisDate=$(date)
    nmcli dev wifi connect "$net"
    sleep 15
    bash ./pinger.sh
    echo ""

    git add *
    git commit -m "wifi-test $thisDate"
    git push
    echo ""
done
