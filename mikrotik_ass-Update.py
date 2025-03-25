import re
import subprocess
import sys
import paramiko
from getpass import getpass

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

required_packages = ['paramiko']
for package in required_packages:
    install_package(package)

def mikrotik_ssh_execute(host, user, password, commands):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=user, password=password)
    for command in commands:
        ssh.exec_command(command)
    ssh.close()

def mikrotik_get_interfaces(host, user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command("/interface print")
    interfaces_output = stdout.read().decode()
    ssh.close()
    interfaces = re.findall(r'^\s*(\d+)\s+[RSXDA\s]*([\w\-]+)\s', interfaces_output, re.MULTILINE)
    return interfaces

def valid_ssh_credentials():
    while True:
        host = input("Mikrotik IP: ")
        user = input("Mikrotik username: ")
        password = getpass("Mikrotik password: ")
        try:
            mikrotik_get_interfaces(host, user, password)
            return host, user, password
        except paramiko.AuthenticationException:
            print("Λάθος username ή password. Προσπάθησε ξανά.")
        except paramiko.SSHException as e:
            print(f"Πρόβλημα σύνδεσης: {e}. Προσπάθησε ξανά.")

def main():
    host, user, password = valid_ssh_credentials()
    interfaces = mikrotik_get_interfaces(host, user, password)
    print("\nΔιαθέσιμα Interfaces:")
    for idx, (iface_num, iface_name) in enumerate(interfaces):
        print(f"{iface_num}: {iface_name}")

    identity = input("\nΒάλε Identity για το Mikrotik: ")
    commands = [f"/system identity set name={identity}"]

    use_dhcp_client = input("Θέλεις να βάλεις DHCP-client; (y/n): ").lower()
    dhcp_client_iface = ""
    if use_dhcp_client == 'y':
        interface_names = [name for _, name in interfaces]
        while True:
            dhcp_client_iface = input("\nΕπέλεξε interface για DHCP-client (δώσε όνομα interface): ")
            if dhcp_client_iface in interface_names:
                break
            else:
                print("Το όνομα δεν είναι έγκυρο. Προσπάθησε ξανά.")
        commands.append(f"/ip dhcp-client add interface={dhcp_client_iface} disabled=no")
        commands.append("/interface list add name=WAN")
        commands.append(f"/interface list member add interface={dhcp_client_iface} list=WAN")
    else:
        wan_iface = input("Δώσε το interface για WAN (δώσε όνομα interface): ")
        wan_ip = input("Δώσε IP address για το WAN interface (π.χ 192.168.1.2/24): ")
        wan_gateway = input("Δώσε Gateway για το WAN: ")
        commands.append(f"/ip address add address={wan_ip} interface={wan_iface}")
        commands.append(f"/ip route add dst-address=0.0.0.0/0 gateway={wan_gateway}")
        commands.append("/interface list add name=WAN")
        commands.append(f"/interface list member add interface={wan_iface} list=WAN")
    print("✅ Δημιουργήθηκε Interface List 'WAN'.")
    commands.append("/ip firewall nat add chain=srcnat action=masquerade out-interface-list=WAN")
    print("✅ NAT masquerade δημιουργήθηκε με out-interface-list 'WAN'.")
    commands.append("/interface list add name=PCC")
    print("✅ Δημιουργήθηκε Interface List 'PCC'.")

    bridge_name = input("Δώσε όνομα για το bridge: ")
    bridge_ip = input("Δώσε IP address για το bridge (default 192.168.88.1/24): ") or "192.168.88.1/24"
    commands += [
        f"/interface bridge add name={bridge_name} protocol-mode=rstp disabled=no",
        f"/ip address add address={bridge_ip} interface={bridge_name}"
    ]

    bridge_interfaces = []
    while True:
        bridge_iface = input("Πληκτρολόγησε interface που θα προσθέσεις στο bridge (enter για τερματισμό): ")
        if not bridge_iface:
            break
        if bridge_iface in [name for _, name in interfaces]:
            bridge_interfaces.append(bridge_iface)
        else:
            print("Άκυρο interface.")

    if not bridge_interfaces:
        print("Δεν επέλεξες κανένα interface για το bridge. Τερματισμός.")
        sys.exit()

    for iface in bridge_interfaces:
        commands.append(f"/interface bridge port add bridge={bridge_name} interface={iface}")

    print("\nDHCP Server Setup")
    ip_base = bridge_ip.split('/')[0]
    ip_prefix = '.'.join(ip_base.split('.')[:3])
    default_dhcp_network = f"{ip_prefix}.0/24"
    default_gateway = ip_base
    default_pool = f"{ip_prefix}.2-{ip_prefix}.254"
    default_dns = "8.8.8.8"
    default_lease_time = "10m"

    print(f"dhcp server interface: {bridge_name}")
    dhcp_network = input(f"dhcp address space (default {default_dhcp_network}): ") or default_dhcp_network
    gateway = input(f"gateway for dhcp network (default {default_gateway}): ") or default_gateway
    pool = input(f"addresses to give out (default {default_pool}): ") or default_pool
    dns = input(f"dns servers (default {default_dns}): ") or default_dns
    lease_time = input(f"lease time (default {default_lease_time}): ") or default_lease_time

    commands += [
        f"/ip pool add name=dhcp_pool ranges={pool}",
        f"/ip dhcp-server add interface={bridge_name} address-pool=dhcp_pool lease-time={lease_time} disabled=no",
        f"/ip dhcp-server network add address={dhcp_network} gateway={gateway} dns-server={dns}"
    ]

    commands.append("/ip cloud set ddns-enabled=yes ddns-update-interval=00:01:00")
    mikrotik_ssh_execute(host, user, password, commands)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=user, password=password)
    stdin, stdout, stderr = ssh.exec_command("/ip cloud print")
    cloud_dns = stdout.read().decode()
    ssh.close()

    print(f"Οι αλλαγές πραγματοποιήθηκαν επιτυχώς!\nΤο DNS name του Mikrotik είναι:\n{cloud_dns}")

if __name__ == "__main__":
    main()
