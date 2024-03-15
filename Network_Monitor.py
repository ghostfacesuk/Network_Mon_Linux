import time

def get_bytes(interface):
    with open('/proc/net/dev', 'r') as f:
        for line in f:
            if interface in line:
                data = line.split(':')
                return int(data[1].split()[0]), int(data[1].split()[8])

def main():
    interface = "eth0"  # Change this to your desired network interface
    print("Monitoring network bandwidth...")
    last_rx, last_tx = get_bytes(interface)
    
    while True:
        rx, tx = get_bytes(interface)
        
        rx_speed = (rx - last_rx) / (1024.0 * 1024.0)  # Received bandwidth in MB/s
        tx_speed = (tx - last_tx) / (1024.0 * 1024.0)  # Sent bandwidth in MB/s
        print(f"Current bandwidth - Received: {rx_speed:.2f} MB/s, Sent: {tx_speed:.2f} MB/s")
        
        last_rx, last_tx = rx, tx
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    main()
