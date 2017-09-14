sudo tcpdump -i eth0 udp port 53 -w outfile.cap &
while true; do python robot.py; sleep 1; done
