from scapy.all import *

def generate_syn_packets(destination_ip, num_packets):
    syn_packets = []
    for _ in range(num_packets):
        syn_packet = IP(dst=destination_ip)/TCP(dport=23, flags="S")
        syn_packets.append(syn_packet)
    send(syn_packets)

destination_ip = '198.51.50.1'
num_packets = 1000 

generate_syn_packets(destination_ip, num_packets)