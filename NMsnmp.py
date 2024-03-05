import subprocess
import re
import json
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import time

def get_ipv4_and_ipv6_addresses(router_ip):
    ipv4_output = subprocess.run(["snmpwalk", "-v2c", "-c", "public", router_ip, "IP-MIB::ipAddressIfIndex.ipv4"], capture_output=True, text=True)
    ipv6_output = subprocess.run(["snmpwalk", "-v2c", "-c", "public", router_ip, "IP-MIB::ipAddressIfIndex.ipv6"], capture_output=True, text=True)

    ipv4_dict = {}
    ipv6_dict = {}

    if ipv4_output.returncode == 0:
        ipv4_lines = ipv4_output.stdout.splitlines()
        for line in ipv4_lines:
            match = re.match(r'IP-MIB::ipAddressIfIndex.ipv4."(.*?)" = INTEGER: (\d+)', line)
            if match:
                ifindex = match.group(2)
                if ifindex == '1':
                    interface = 'Fa0/0'
                elif ifindex == '2':
                    interface = 'Fa1/0'
                else:
                    interface = f'Unknown{ifindex}'
                ipv4_dict[interface] = match.group(1)

    if ipv6_output.returncode == 0:
        ipv6_lines = ipv6_output.stdout.splitlines()
        for line in ipv6_lines:
            match = re.match(r'IP-MIB::ipAddressIfIndex.ipv6."(.*?)" = INTEGER: (\d+)', line)
            if match:
                ifindex = match.group(2)
                if ifindex == '1':
                    interface = 'Fa0/0'
                elif ifindex == '2':
                    interface = 'Fa1/0'
                else:
                    interface = f'Unknown{ifindex}'
                ipv6_dict[interface] = match.group(1)

    return ipv4_dict, ipv6_dict

def get_interface_status(router_ip):
    status_output = subprocess.run(["snmpwalk", "-v2c", "-c", "public", router_ip, "1.3.6.1.2.1.2.2.1.8"], capture_output=True, text=True)

    status_dict = {}

    if status_output.returncode == 0:
        status_lines = status_output.stdout.splitlines()
        for line in status_lines:
            match = re.match(r'IF-MIB::ifOperStatus.(\d+) = INTEGER: (up|down)', line)
            if match:
                ifindex = match.group(1)
                status = match.group(2)
                if ifindex == '1':
                    interface = 'Fa0/0'
                    status_dict[interface] = status
                elif ifindex == '2':
                    interface = 'Fa1/0'
                    status_dict[interface] = status

    return status_dict

def get_cpu_utilization(router_ip):
    cpu_output = subprocess.run(["snmpget", "-v2c", "-c", "public", router_ip, "1.3.6.1.4.1.9.9.109.1.1.1.1.10.1"], capture_output=True, text=True)
    if cpu_output.returncode == 0:
        match = re.match(r'SNMPv2-SMI::enterprises.9.9.109.1.1.1.1.10.1 = Gauge32: (\d+)', cpu_output.stdout)
        if match:
            return int(match.group(1))
    return None


def get_interface_details():
    routers = {
        'R1': '198.51.50.1',
        'R2': '198.51.200.2',
        'R3': '198.51.200.3',
        'R4': '198.51.100.1',
        'R5': '198.51.200.5'
    }

    output = {}
    for router, ip in routers.items():
        ipv4_dict, ipv6_dict = get_ipv4_and_ipv6_addresses(ip)
        status_dict = get_interface_status(ip)
        addresses = {}
        for interface, ipv4 in ipv4_dict.items():
            addresses[interface] = {"v4": ipv4, "v6": ipv6_dict.get(interface, "")}
        status_formatted = {f"{index}": status for index, status in status_dict.items()}
        output[router] = {"addresses": addresses, "status": status_formatted}

    with open('interface_details.txt', 'w') as file:
        json.dump(output, file, indent=4)

    print("Output written to interface_details.txt file.")

    #CPU Utilization

    duration = 120  # 2 minutes
    interval = 5  # 5 seconds

    cpu_utilization = []
    timestamps = []

    start_time = time.time()
    while time.time() - start_time < duration:
        cpu = get_cpu_utilization('198.51.50.1')
        if cpu is not None:
            cpu_utilization.append(cpu)
            timestamps.append(pd.Timestamp.now())
            print(f"Timestamp: {pd.Timestamp.now()}, CPU Utilization: {cpu}%\n")
        time.sleep(interval)

    df = pd.DataFrame({'Timestamp': timestamps, 'CPU Utilization': cpu_utilization})

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['CPU Utilization'], mode='lines', name='CPU Utilization'), secondary_y=False)
    fig.update_xaxes(title_text='Time')
    fig.update_yaxes(title_text='CPU Utilization (%)', secondary_y=False)
    fig.update_layout(title='CPU Utilization of R1')
    fig.write_image('cpu_utilization_plot.jpg')

    fig.show()

if __name__ == "__main__":
    get_interface_details()