# Network Monitor For Linux

## Python
- Reads the /proc/net/dev file, parses it to find the relevant interface, and calculates the bandwidth usage based on the difference between consecutive readings.

## Behaviour & Usage
- Select NIC from list by selecting the corresponding number.
- If the network bandwith exceeds 5 MB/s a .txt file will be created and the results captured. When the bandwidth falls below 2MB/s for more than 10s the file will close.
- Press 'q' to quit the application. 
