cd /var/lib/cloud9/ENGI301/LEDscape
config-pin P1_08 out
config-pin -q P1_08
sudo ./opc-server --config my-config.json

python3 drive.py