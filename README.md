#Createwifi
Using the shortest codes and simplest params to create wifi hotspot

I know there are plenty of programs can help to create WiFi hotspots, but most of them are complex to use and modify. 

##Dependencies
For Kali:
```
apt install hostapd dnsmasq
```

##Useage
```
python createwifi.py -e "OpenWiFi"
python createwifi.py -e "OpenWiFi" -i wlan0 -o eth0 -c channel

python createwifi.py -e "WPAWiFi" -p 12345678
python createwifi.py -e "WPAWiFi"  -i wlan0 -o eth0 -c channel -p 12345678
```
