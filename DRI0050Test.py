# -*- coding: utf-8 -*-
'''
PWM frequency higher than 2K, there may be relatively large difference between the frequency and the set value. 
For frequency higher than 2K, please refer to the following frequency value: 
46875HZ, 23437HZ, 15625HZ, 11718HZ,
9375HZ, 7812HZ, 6696HZ, 5859HZ, 5208HZ, 4687HZ, 4261HZ,
3906HZ, 3605HZ, 3348HZ, 3125HZ,
2929HZ, 2757HZ, 2604HZ, 2467HZ, 2343HZ, 2232HZ, 2130HZ, 2038HZ,
'''

import time
from serial import *
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# PORT="COM12" #Windows platform
PORT="/dev/ttyUSB0" #Linux platform
BAUDRATE=9600
SLAVE_ADDR=0x32



PID_REG       =  0x00
VID_REG       =  0x01
ADDR_REG      =  0x02
VER_REG       =  0x05
DUTY_REG      =  0x06
FREQ_REG      =  0x07
PWM_EN_REG    =  0x08

ser = Serial(port=PORT,baudrate=BAUDRATE, bytesize=8, parity='N', stopbits=1)
print("here")
master = modbus_rtu.RtuMaster(ser)
time.sleep(0.5)

def get_pid():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, PID_REG, 1)
  time.sleep(0.03)
  return data[0]

def get_vid():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, VID_REG, 1)
  time.sleep(0.03)
  return data[0]

def get_addr():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, ADDR_REG, 1)
  time.sleep(0.03)
  return data[0]

def get_version():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, VER_REG, 1)
  time.sleep(0.03)
  return data[0]

def get_duty():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, DUTY_REG, 1)
  time.sleep(0.03)
  return data[0]/255

def get_freq():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, FREQ_REG, 1)
  time.sleep(0.03)
  return int(12*1000*1000/256/(data[0]+1))

def get_enable():
  data = master.execute(SLAVE_ADDR, cst.READ_HOLDING_REGISTERS, PWM_EN_REG, 1)
  time.sleep(0.03)
  return data[0]

def set_duty(duty):
  master.execute(SLAVE_ADDR, cst.WRITE_SINGLE_REGISTER, DUTY_REG, output_value=int(duty*255))
  time.sleep(0.03)

def set_freq(freq):
  master.execute(SLAVE_ADDR, cst.WRITE_SINGLE_REGISTER, FREQ_REG, output_value=int(12*1000*1000/256/freq) - 1)
  time.sleep(0.03)

def set_enable(enable):
  master.execute(SLAVE_ADDR, cst.WRITE_SINGLE_REGISTER, PWM_EN_REG, output_value=enable)
  time.sleep(0.03)

def pwm(freq, duty):
  v=[]
  v.append(int(duty*255))
  v.append(int(12*1000*1000/256/freq) - 1)
  master.execute(SLAVE_ADDR, cst.WRITE_MULTIPLE_REGISTERS, DUTY_REG, output_value=v)
  time.sleep(0.03)


print("version=0x{:x}, addr=0x{:x}".format(get_version(), get_addr()))
print("pid=0x{:x}, vid=0x{:x}".format(get_vid(), get_pid()))

print("\n--------Initial Value------") 
print("freq={}, duty={:.2f} enable={}".format(get_freq(), get_duty(), get_enable()))  

print("--------Set a new value------")  
#pwm(freq=860,duty=0.82) # freq(183HZ-46875HZ) duty(0%-100%)
set_freq(860) #(183HZ-46875HZ)
set_duty(0.82)#(0%-100%)
set_enable(1)
print("freq={}, duty={:.2f} enable={}".format(get_freq(), get_duty(), get_enable()))

print("--------Restore to factory settings(366HZ, duty ratio 50%, diable output)-------\n")
pwm(freq=366, duty=0.5) # freq(183HZ-46875HZ) duty(0%-100%)
set_enable(0)
