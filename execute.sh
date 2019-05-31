sudo tcpdump -i eth0 udp port 53 -w outfile.pcap &
while true; do python robot.py; sleep 100; done
