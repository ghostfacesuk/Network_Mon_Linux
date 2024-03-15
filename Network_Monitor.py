import os
import time

def list_network_interfaces():
    # Get a list of available network interfaces
    interfaces = os.listdir('/sys/class/net')
    return interfaces

def get_bytes(interface):
    with open('/proc/net/dev', 'r') as f:
        for line in f:
            if interface in line:
                data = line.split(':')
                return int(data[1].split()[0]), int(data[1].split()[8])
        raise ValueError(f"Network interface '{interface}' not found.")

def main():
    # List available network interfaces
    interfaces = list_network_interfaces()
    print("Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}. {iface}")
    
    # Prompt user to select an interface
    while True:
        try:
            choice = int(input("Enter the number corresponding to the desired interface: "))
            if 1 <= choice <= len(interfaces):
                interface = interfaces[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    print(f"Monitoring network bandwidth for interface {interface}...")
    
    try:
        last_rx, last_tx = get_bytes(interface)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    while True:
        try:
            rx, tx = get_bytes(interface)
        except ValueError as e:
            print(f"Error: {e}")
            break
        
        rx_speed = (rx - last_rx) / (1024.0 * 1024.0)  # Received bandwidth in MB/s
        tx_speed = (tx - last_tx) / (1024.0 * 1024.0)  # Sent bandwidth in MB/s
        print(f"Current bandwidth - Received: {rx_speed:.2f} MB/s, Sent: {tx_speed:.2f} MB/s")
        
        last_rx, last_tx = rx, tx
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    main()
