import scapy.all as scapy
from scapy_http import http
import optparse


def get_input():

    parse = optparse.OptionParser()

    parse.add_option("-i", "--interface", dest="interf", help="Interface Name")

    option = parse.parse_args()[0]

    return option.interf


def listener(arg):

    scapy.sniff(iface=arg, store=False, prn=analyze)


def analyze(packet):

    if packet.haslayer(http.HTTPRequest):

        if packet.haslayer(scapy.Raw):

            print(packet[scapy.Raw].load)


interface = get_input()
listener(interface)
