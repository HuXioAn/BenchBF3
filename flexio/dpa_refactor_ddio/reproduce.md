# Reproduce DPA DDIO


Compile the project on host, you'll find the ELF `dpa_refactor_ddio` under folder `bin_host`. 


``` shell
# Adjust the Macros in dpa_refacter_common.h for setups
./dpa_refactor_ddio --device_name mlx5_0 > 512_1KB.log
./dpa_refactor_ddio --device_name mlx5_0 > 4096_128B.log

# launch then it waits for the packets

```

## Packet Generator

Use `pktgen` for sending the packets to the DPA. Here, I use hsn0, which is an Intel E810-C to send to the BF3.

``` shell

sudo modprobe pktgen
echo "add_device hsn0" | sudo tee /proc/net/pktgen/kpktgend_0


DEV=/proc/net/pktgen/hsn0

echo "count 512"        | sudo tee $DEV # to be adjusted
echo "pkt_size 1024"    | sudo tee $DEV # to be adjusted   
echo "delay 0"          | sudo tee $DEV
echo "clone_skb 0"      | sudo tee $DEV
echo "dst_mac 58:a2:e1:bc:08:e2" | sudo tee $DEV # should be the BF3 MAC

echo "start" | sudo tee /proc/net/pktgen/pgctrl # Trigger one send

sudo bash -c '
for ((i=0; i<512; i++)); do # should be adjusted too
    echo start > /proc/net/pktgen/pgctrl
    sleep 1 # with a long delay, we dont need to sync 
done
'

```

-------

Then you should see the log pop up every second, then when it reaches the last one, use Ctrl+C to finish it.




