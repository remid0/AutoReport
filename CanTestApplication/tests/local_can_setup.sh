#!/bin/bash

# Shell script which sets up the virtual can channels for local debug
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

sudo modprobe vcan
sudo ip link add dev vcan1 type vcan
sudo ip link set up vcan1

ifconfig