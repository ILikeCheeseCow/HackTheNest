import serial
import time

# Establish the connection on a specific port
ser = serial.Serial('COM5', 9600)  # Replace 'COM5' with your Arduino's port
time.sleep(2)  # Wait for the connection to establish

def send_command(command):
    ser.write(command.encode())
    time.sleep(1)  # Wait for Arduino to process the command

def move_forward():
    send_command('f')

def move_backward():
    send_command('b')

def stop():
    send_command('s')

def close_connection():
    ser.close()  # Close the serial connection

def move_backward_half():
    send_command('bh')

