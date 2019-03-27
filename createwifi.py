# author: qingxp9
# python createwifi.py -e ssid -i wlan0 -o eth0 -c channel

from argparse import ArgumentParser
import os

def set_configs():
    parser = ArgumentParser()
    parser.add_argument('-e',
                  dest='essid',
                  default='MyWiFi',
                  type=str,
                  help='Wi-Fi name')

    parser.add_argument('-o',
                  dest='output',
                  default='eth0',
                  type=str,
                  help='the interface of the output')

    parser.add_argument('-i',
                  dest='iface',
                  default='wlan0',
                  type=str,
                  help='the interface of the AP')

    parser.add_argument('-c',
                  dest='channel',
                  default='11',
                  type=str,
                  help='AP channel')

    parser.add_argument('-p',
                  dest='password',
                  default='',
                  type=str,
                  help=' WiFi Password, length shoud be >= 8')

    args = parser.parse_args()

    if len(args.password) < 8 and len(args.password) !=0:
        print("[Error] The length of WPA passphrase should be longer than 8")
        parser.print_help()
        os._exit(0)

    return {
        'iface' : args.iface,
        'essid' : args.essid,
        'channel' : args.channel,
        'output': args.output,
        'password': args.password
    }
def dnsmasq(iface):
    os.system("systemctl stop dnsmasq")
    os.system("killall dnsmasq")
    os.system("echo 'dhcp-range=172.5.10.100,172.5.10.250,12h' > dnsmasq.conf")
    os.system("echo 'interface=" + iface +"' >> dnsmasq.conf")
    os.system("dnsmasq -C dnsmasq.conf  -l dnsmasq.leases")

def iptables(iface, output):
    os.system("ifconfig " + output + " up")
    #os.system("dhclient " + output)
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    os.system("iptables -F")
    os.system("iptables -t nat -F")
    os.system("ifconfig " + iface + " up")
    os.system("iptables -t nat -A POSTROUTING -o " + output + " -j MASQUERADE")

def hostapd(iface, essid, channel, password):
    # Make Configuration File
    os.system("echo 'interface=" + iface + "' > hostapd.conf")
    os.system("echo 'ssid=" + essid + "' >> hostapd.conf")
    os.system("echo 'driver=nl80211' >> hostapd.conf")
    os.system("echo 'channel=" + channel + "' >> hostapd.conf")
    os.system("echo 'hw_mode=g' >> hostapd.conf")
    if password:
        os.system("echo 'auth_algs=1' >> hostapd.conf") # 1=wpa, 2=wep, 3=both
        os.system("echo 'wpa=2' >> hostapd.conf") # 1=wpa1, 2=wpa2, 3=both
        os.system("echo 'wpa_key_mgmt=WPA-PSK' >> hostapd.conf")
        os.system("echo 'rsn_pairwise=CCMP' >> hostapd.conf")
        os.system("echo 'wpa_passphrase=" + password + "' >> hostapd.conf")

    # Running hostapd
    os.system("nmcli radio wifi off")
    os.system("rfkill unblock wlan")
    os.system("ifconfig " + iface + " 172.5.10.1/24")
    os.system("hostapd hostapd.conf")

if __name__ == '__main__':
    confs = set_configs()
    iface = confs["iface"]
    output = confs["output"]
    essid = confs["essid"]
    channel = confs["channel"]
    password = confs["password"]

    #DNS and DHCP server
    dnsmasq(iface)
    #iptables
    iptables(iface, output)
    #hostapd config
    hostapd(iface, essid, channel, password)



