#!/usr/bin/env python
import subprocess


def bash(command):
    return subprocess.check_output(['bash', '-c', command])

def nmap_scan(ip):
    print("Scanning TCP ports on " + ip)
    print("------------------------------------\n")
    res = bash('nmap -T4 -p1-65535 %s | grep"open"' % ip).splitlines()
    ports = []

    for port in res:
        print(port)
        ports.append(port.split("/")[0])

    port_list = ",".join(ports)

    print("Running Intense scan on open ports...\n")
    bash("nmap -T4 -A -sV -p%s -oN output.txt %s" % (port_list, ip))
    print("Nmap Intense scan result logged in output.txt")
    exit()


ip_string = bash('ifconfig wlan0 | grep "inet "')
ip = ip_string.strip().split(" ")[1]

octets = ".".join(ip.split(".")[:-1])
subnet = octets + ".0/24"

print("\nRunning netdiscover on local subnet: %s " % subnet)
print("----------------------------------------------------\n")
ips = bash('netdiscover -P -r %s | grep "1" | cut -d " " -f2' % subnet).splitlines()
for i in range(0, len(ips)):
    ip = ips[i]
    print("%s. %s" %(i + 1, ip))

choice = input("Enter an option 1 - %s or 0 to exit: " % len(ips))

nmap_scan(ips[choice - 1])
