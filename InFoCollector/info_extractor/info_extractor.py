import platform
import uuid
import getpass
import psutil
import socket
import ctypes
import os
import requests
import uptime
import re
import sys
system_info:'str'=""
interfaces_info:'str'=""
ip_info:'str'=""
def extract_system_info()->'str':
    """
    This function extracts General os related info.
    """
    global system_info
    info:'tuple'=platform.uname()
    system_info=f"OS Name: {info[0]}\nHost Name :{info[1]}\nrelease: {info[2]}\nOS Version: {info[3]}\nMachine Architecture: {info[4]}\n"
    system_info+=f"UUID: {uuid.uuid1()}\n"
    try:
        system_info+=f"Username: {getpass.getuser()}\n"
    except OSError:
        print("THe user name can not be retrieved\n")
    is_admin:'bool'=False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    system_info+=("Privilege: Admin/root" if is_admin else "Privilege: NotAdmin/root\n")
    #getting the boottime and uptime:
    system_info+=f"Boot time : {uptime.boottime()}\nUptime: "
    #calculating uptime:
    uptime_seconds=uptime.uptime()
    system_info+=f"{int(uptime_seconds//3600)}:"
    uptime_seconds%=3600
    system_info += f"{int(uptime_seconds // 60)}:"
    uptime_seconds %= 60
    system_info += f"{int(uptime_seconds*100)//100}\n"
def extract_interfaces_info()->'None':
    """This function enumerates all network interfaces ,and their respective addresses"""
    global interfaces_info
    accumelator=[]
    info=psutil.net_if_addrs()
    accumelator.append("-" * 80 +"\n")
    for interface_name,addresses in info.items():
        accumelator.append(f"Interface name :{interface_name}\n")
        for address in addresses:
            if address.family==2:
                accumelator.append(f"Ipv4 :{address.address}, netmask:{address.netmask}, broadcast:{address.broadcast}\n")
            elif address.family==10:
                accumelator.append(f"Ipv6 :{address.address},netmask:{address.netmask},broadcast:{address.broadcast}\n")
            elif address.family==17:
                accumelator.append(f"MAC address: {address.address}\n\n\n")
            interfaces_info=''.join(accumelator)
        accumelator.append("-" * 80 + "\n")
def show_help()->'None':
    pass
def extract_ipaddress_info()->'None':
    global ip_info
    reply = requests.get("https://ipwho.is/")
    while (reply.status_code>=400) and (reply.status_code<=599):
        reply = requests.get("https://ipwho.is/")
    reply = reply.json()
    ip_info+="-" * 80 + "\n\n"
    if reply["type"]=="IPv4":
        ip_info+=f"Public IPv4 Address: {reply['ip']}\n"
    if reply["type"]=="IPv6":
        ip_info+=f"Public IPv6 Address: {reply['ip']}\n"

    #geolocation:
    ip_info+=f"Continent: {reply["continent"]} ,Country: {reply["country"]} {reply["flag"]["emoji"]},{reply["region"]},{reply["city"]}\nPostal Code: {reply["postal"]},Calling Code: +{reply["calling_code"]}\n"
    ip_info+=f"Geolocation->Longitude: {reply["longitude"]}\tLatitude: {reply["latitude"]}\n"
    #isp info:
    ip_info+=f"Organization: {reply['connection']['org']},ISP: {reply['connection']['isp']},ISP domain:{reply['connection']['domain']}\n\n"
    #time zone info:
    ip_info+=f"{reply['timezone']['id']} UTC{reply['timezone']['utc']} , Current time:{reply['timezone']['current_time']}\n"
def check_args(argument_string:'str')->'bool':
    match:'bool'=bool(re.match(r"^((?:--help|-h)|(?:-s|--system)|(?:-a|--all)|(?:-nt|--interface)|(-i|--ip)|((?:-s|--system)?\s+(?:-nt|--interface)?\s*(?:-i|--ip)?)|((?:-nt|--interface)?\s+(?:-s|--system)?\s*(?:-i|--ip)?)|((?:-nt|--interface)?\s+(?:-i|--ip)?\s*(?:-s|--system)?)|((?:-i|--ip)?\s+(?:-nt|--interface)?\s*(?:-s|--system)?)|((?:-i|--ip)?\s+(?:-s|--system)?\s*(?:-nt|--interface)?)|((?:-s|--system)?\s+(?:-i|--ip)?\s*(?:-nt|--interface)?))$",argument_string))
    return match
def argparser(argument_string: 'str') -> 'list':
    return argument_string.split()
def main():
    global system_info,interfaces_info,ip_info
    args=sys.argv[1:]
    extract_ipaddress_info();extract_system_info();extract_interfaces_info()
    argument_string:'str'=' '.join(args)
    provided_args:'list'=argparser(argument_string)
    if check_args(argument_string):
        for arg in provided_args:
            if arg=="-h" or arg=="--help":
                show_help()
                sys.exit(0)
            elif arg=="-a" or arg=="--all":
                print(system_info,interfaces_info,ip_info,sep="\n")
                sys.exit(0)
            elif arg=="-s" or arg=="--system":
                print(system_info)
            elif arg=="-nt" or arg=="--interface":
                print(interfaces_info)
            elif arg=="-i" or arg=="--ip":
                print(ip_info)
    else:
        raise SystemExit(show_help())
if __name__=="__main__":
    main()
