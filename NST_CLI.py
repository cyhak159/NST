import socket
import argparse

print("""
███╗░░██╗████████╗░██████╗  ░█████╗░██╗░░░░░██╗
████╗░██║╚══██╔══╝██╔════╝  ██╔══██╗██║░░░░░██║
██╔██╗██║░░░██║░░░╚█████╗░  ██║░░╚═╝██║░░░░░██║
██║╚████║░░░██║░░░░╚═══██╗  ██║░░██╗██║░░░░░██║
██║░╚███║░░░██║░░░██████╔╝  ╚█████╔╝███████╗██║
╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░  ░╚════╝░╚══════╝╚═╝""")

def scan_ports(target_host, start_port, end_port, show_info):
    open_ports = []

    for port in range(start_port, end_port + 1):
        result = scan_port(target_host, port)
        if result == 0:
            open_ports.append(port)
            if show_info:
                service_name = get_service_name(port)
                print(f"Port {port} is open - Service: {service_name}")
    
    if not open_ports:
        print("No open ports found.")
    
    return open_ports

def scan_port(target_host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Adjust the timeout as needed
            result = s.connect_ex((target_host, port))
            return result
    except (socket.timeout, ConnectionRefusedError):
        return None
    except socket.error as e:
        print(f"Error occurred while scanning port {port}: {e}")
        return None

def get_service_name(port):
    # You can implement a service name lookup here using a dictionary or a service lookup library
    # For simplicity, we'll just return the port number as the service name.
    return str(port)

def main():
    parser = argparse.ArgumentParser(description="Port Scanner Tool")
    parser.add_argument("target_host", help="Target host or IP address")
    parser.add_argument("start_port", type=int, help="Start port number")
    parser.add_argument("end_port", type=int, help="End port number")
    parser.add_argument("--show-info", action="store_true", help="Show service info for open ports")
    parser.add_argument("--export", metavar="FILENAME", help="Export open ports info to a text file")

    args = parser.parse_args()

    print(f"Scanning ports on {args.target_host} from {args.start_port} to {args.end_port}...")

    open_ports = scan_ports(args.target_host, args.start_port, args.end_port, args.show_info)

    if open_ports:
        print("Open ports:")
        print(open_ports)

    if args.export:
        export_ports_info(args.export, open_ports)

def export_ports_info(filename, open_ports):
    if open_ports:
        with open(filename, "w") as file:
            file.write("Open ports:\n")
            file.write("\n".join(map(str, open_ports)))
            print(f"Open ports information saved to {filename}")
    else:
        print("No open ports to export.")

if __name__ == "__main__":
    main()
