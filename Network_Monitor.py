import os
import sys
import time
import select

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

def get_output_filename():
    # Get current system time and date
    current_time = time.localtime()
    filename = f"{current_time.tm_hour:02d}{current_time.tm_min:02d}_{current_time.tm_mday:02d}{current_time.tm_mon:02d}{current_time.tm_year}.txt"
    return filename

def main():
    # List available network interfaces
    interfaces = list_network_interfaces()
    print("Available network interfaces:")
    for i, iface in enumerate(interfaces):
        print(f"{i + 1}. {iface}")
    
    # Prompt user to select an interface
    while True:
        try:
            choice = input("Enter the number corresponding to the desired interface: ")
            if choice.lower() == 'q':
                print("Monitoring stopped.")
                return
            choice = int(choice)
            if 1 <= choice <= len(interfaces):
                interface = interfaces[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid number or 'q' to quit.")
        except ValueError:
            print("Invalid input. Please enter a valid number or 'q' to quit.")
    
    print(f"Monitoring network bandwidth for interface {interface}...")
    
    try:
        last_rx, last_tx = get_bytes(interface)
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    output_file = None
    test_started = False
    low_speed_counter = 0
    
    while True:
        try:
            rx, tx = get_bytes(interface)
        except ValueError as e:
            print(f"Error: {e}")
            break
        
        rx_speed = (rx - last_rx) / (1024.0 * 1024.0)  # Received bandwidth in MB/s
        tx_speed = (tx - last_tx) / (1024.0 * 1024.0)  # Sent bandwidth in MB/s
        
        if rx_speed >= 5 or tx_speed >= 5:
            if not test_started:
                print("Test start")
                filename = get_output_filename()
                output_file = open(filename, "w")
                output_file.write("Test start\n")
                test_started = True
                low_speed_counter = 0
        elif test_started:
            low_speed_counter += 1
            if low_speed_counter >= 10:
                print("Test stopped")
                if output_file:
                    output_file.write("Test stopped\n")
                    output_file.close()
                    output_file = None
                test_started = False
        
        if test_started or (not test_started):  # Always print to terminal regardless of test_started
            print(f"Current bandwidth - Received: {rx_speed:.2f} MB/s, Sent: {tx_speed:.2f} MB/s")
            if output_file and test_started:
                output_file.write(f"Current bandwidth - Received: {rx_speed:.2f} MB/s, Sent: {tx_speed:.2f} MB/s\n")
        
        last_rx, last_tx = rx, tx
        
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            if line.lower() == 'q':
                print("Monitoring stopped.")
                if output_file:
                    output_file.close()
                return

        time.sleep(1)  # Update every second

    if output_file:
        output_file.close()

if __name__ == "__main__":
    main()
