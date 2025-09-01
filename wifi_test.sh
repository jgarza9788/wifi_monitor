networks=(
    "Error 404" 
    "Error 404_EXT" 
<<<<<<< HEAD
    "Error 404 NH" 
=======
    # "Error 404 NH" 
>>>>>>> 506941fff25ebe70dbf93d13611fd8fd8b88bd57
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
<<<<<<< HEAD
=======

nmcli dev wifi connect "Error 404_EXT" 
>>>>>>> 506941fff25ebe70dbf93d13611fd8fd8b88bd57
