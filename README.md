# INSTALL
```
git clone https://github.com/eni23/collect-oscp-logs
cd collect-oscp-logs/
cp collect-oscp-logs.py /usr/local/bin/collect-oscp-logs
chmod a+x /usr/local/bin/collect-oscp-logs
cp collect-oscp-logs.service /etc/systemd/system/
cp collect-oscp-logs.timer /etc/systemd/system/
mkdir /var/log/oscp-logs

systemctl daemon-reload
systemctl enable collect-oscp-logs.timer
systemctl start collect-oscp-logs.timer

systemctl list-timers
```
