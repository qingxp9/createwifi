# Createwifi
Using the shortest codes and simplest params to create wifi hotspot

I know there are plenty of programs can help to create WiFi hotspots, but most of them are complex to use and modify. 

## Dependencies
For Kali:
```
apt install hostapd dnsmasq
```

## Usage
```
#without password and Internet
python createwifi.py -e "OpenWiFi"
#with password and Internet
python createwifi.py -e "WPAWiFi" -p 12345678 -o eth0
##All options
python createwifi.py -e "WPAWiFi" -i wlan0 -o eth0 -c channel -p 12345678
```
