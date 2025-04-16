import time
import socket
from radar_config import SerialConfig
from real_time_process import UdpListener
from queue import Queue

# Step 1: Setup Radar Configuration
config_file = "../config/IWR1843_cfg.cfg"  # Change path if needed
#config_file = "../config/myspeechconfig.cfg" 
radar = SerialConfig("ConnectRadar", "COM4", 115200)

print("\nStopping any existing radar process...")
radar.StopRadar()
time.sleep(1)

print("\nSending configuration file...")
radar.SendConfig(config_file)
time.sleep(1)  # Allow time for config

print("\nStarting radar...")
radar.StartRadar()
time.sleep(1)

# Step 2: Configure DCA1000 FPGA (Required for Data Output)
config_address = ('192.168.33.30', 4096)  # Host PC (receiver)
FPGA_address_cfg = ('192.168.33.180', 4096)  # FPGA address
cmd_order = ['9', 'E', '3', 'B', '5']  # DO NOT send '6' (stop recording)

# Initialize UDP socket for FPGA configuration
sockConfig = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockConfig.bind(config_address)

def send_cmd(code):
    # command code list
    CODE_1 = (0x01).to_bytes(2, byteorder='little', signed=False)
    CODE_2 = (0x02).to_bytes(2, byteorder='little', signed=False)
    CODE_3 = (0x03).to_bytes(2, byteorder='little', signed=False)
    CODE_4 = (0x04).to_bytes(2, byteorder='little', signed=False)
    CODE_5 = (0x05).to_bytes(2, byteorder='little', signed=False)
    CODE_6 = (0x06).to_bytes(2, byteorder='little', signed=False)
    CODE_7 = (0x07).to_bytes(2, byteorder='little', signed=False)
    CODE_8 = (0x08).to_bytes(2, byteorder='little', signed=False)
    CODE_9 = (0x09).to_bytes(2, byteorder='little', signed=False)
    CODE_A = (0x0A).to_bytes(2, byteorder='little', signed=False)
    CODE_B = (0x0B).to_bytes(2, byteorder='little', signed=False)
    CODE_C = (0x0C).to_bytes(2, byteorder='little', signed=False)
    CODE_D = (0x0D).to_bytes(2, byteorder='little', signed=False)
    CODE_E = (0x0E).to_bytes(2, byteorder='little', signed=False)

    # packet header & footer
    header = (0xA55A).to_bytes(2, byteorder='little', signed=False)
    footer = (0xEEAA).to_bytes(2, byteorder='little', signed=False)

    # data size
    dataSize_0 = (0x00).to_bytes(2, byteorder='little', signed=False)
    dataSize_6 = (0x06).to_bytes(2, byteorder='little', signed=False)

    # data
    data_FPGA_config = (0x01020102031e).to_bytes(6, byteorder='big', signed=False)
    data_packet_config = (0xc005350c0000).to_bytes(6, byteorder='big', signed=False)

    # connect to DCA1000
    connect_to_FPGA = header + CODE_9 + dataSize_0 + footer
    read_FPGA_version = header + CODE_E + dataSize_0 + footer
    config_FPGA = header + CODE_3 + dataSize_6 + data_FPGA_config + footer
    config_packet = header + CODE_B + dataSize_6 + data_packet_config + footer
    start_record = header + CODE_5 + dataSize_0 + footer
    stop_record = header + CODE_6 + dataSize_0 + footer

    if code == '9':
        re = connect_to_FPGA
    elif code == 'E':
        re = read_FPGA_version
    elif code == '3':
        re = config_FPGA
    elif code == 'B':
        re = config_packet
    elif code == '5':
        re = start_record
    elif code == '6':
        re = stop_record
    else:
        re = 'NULL'
    # print('send command:', re.hex())
    return re

print("\nConfiguring DCA1000 FPGA...")
for cmd in cmd_order:
    sockConfig.sendto(send_cmd(cmd), FPGA_address_cfg)
    time.sleep(0.1)
    response, _ = sockConfig.recvfrom(2048)
    print(f"Sent command {cmd}, response: {response.hex()}")

sockConfig.close()
print("FPGA Configuration Complete.\n")

adc_sample = 64
chirp = 32
tx_num = 1
rx_num = 4
radar_config = [adc_sample, chirp, tx_num, rx_num]
frame_length = adc_sample * chirp * tx_num * rx_num * 2



# Step 3: Start UDP Listener
BinData = Queue()
udp_listener = UdpListener("Listener", BinData, frame_length, ('192.168.33.30', 4098), 2097152)
udp_listener.start()

# Step 4: Check if Data is Received
print("\nChecking if radar is sending data...")
timeout = time.time() + 10  # 10-second timeout
data_received = False

while time.time() < timeout:
    if not BinData.empty():
        data = BinData.get()
        print(f"Received {len(data)} data points from radar!")
        data_received = True
        break
    time.sleep(0.5)

# Step 5: Print Results
if data_received:
    print("\nSUCCESS: Radar is sending data!")
else:
    print("\nERROR: No data received from radar! Check network settings.")

# Step 6: Stop the radar
print("\nStopping radar...")
radar.StopRadar()
time.sleep(1)



