#!/usr/bin/python3
import ina219
import gpiozero
import time
import serial
import subprocess

results = {}
results['pass'] = 0
results['fail'] = 0

SHUNT_OHMS = 0.1

def read_power():
    results = {}
    results['voltage'] = ina.voltage()
    results['current'] = ina.current()
    return results

# Current sensor
ina = ina219.INA219(SHUNT_OHMS)
ina.configure()

# VTarget enable
vtarget_en = gpiozero.LED(13)
vtarget_en.off()
time.sleep(1)

# buffered UART
uart = serial.Serial("/dev/serial0", 115200, timeout=.2)


# Test that no voltage is present while off
val = read_power()
print(val)
if (val['voltage'] > .05):
    print('target voltage (off) fail')
    results['fail'] += 1
else:
    print('target voltage (off) ok')
    results['pass'] += 1

if (val['current'] > .05):
    print('target current (off) fail')
    results['fail'] += 1
else:
    print('target current (off) ok')
    results['pass'] += 1

# Test that serial doesn't work while off
uart.write(b"hey")
val = uart.read(3)
print({val})
if val != b"":
    print('UART RX(off) fail')
    results['fail'] += 1
else:
    print('UART RX(off) ok')
    results['pass'] += 1


# Enable power
vtarget_en.on()
time.sleep(1)

# Test that voltage and current present while on
val = read_power()
print(val)
if (val['voltage'] > 3.4) or (val['voltage'] < 3.2):
    print('target voltage (on) fail')
    results['fail'] += 1
else:
    print('target voltage (on) ok')
    results['pass'] += 1

if (val['current'] > 100) or (val['current'] < 40):
    print('target current (on) fail')
    results['fail'] += 1
else:
    print('target current (on) ok')
    results['pass'] += 1

# Test that serial loopback works while on (requires jumper from TX to RX)
uart.write(b"hey")
val = uart.read(3)
print({val})
if val != b"hey":
    print('UART RX(on) fail')
    results['fail'] += 1
else:
    print('UART RX(on) ok')
    results['pass'] += 1

# Test that a target can be probed using JTAG
command = [
  "sudo",
  "openocd",
  "-f", "jtag_hat.cfg",
  "-c", "bindto 0.0.0.0; transport select jtag",
  "-c", "adapter speed 1000",
  "-f", "target/stm32f1x.cfg",
  "-c", "init; exit"
  ]

s = open('result-jtag.log','w')
e = open('errorresult-jtag.log','w')
val = subprocess.call(command, stdout=s, stderr=e)
s.close()
e.close()
if (val != 0):
    print('JTAG test fail')
    results['fail'] += 1
else:
    print('JTAG test ok')
    results['pass'] += 1


# Test that a target can be probed using SWD
command = [
  "sudo",
  "openocd",
  "-f", "jtag_hat.cfg",
  "-c", "bindto 0.0.0.0; transport select swd",
  "-c", "adapter speed 1000",
  "-f", "target/stm32f1x.cfg",
  "-c", "init; exit"
  ]


s = open('result-swd.log','w')
e = open('errorresult-swd.log','w')
val = subprocess.call(command, stdout=s, stderr=e)
s.close()
e.close()
if (val != 0):
    print('SWD test fail')
    results['fail'] += 1
else:
    print('SWD test ok')
    results['pass'] += 1


print(results)

print('test done, running reset toggle for manual verification')

srst = gpiozero.LED(24)
trst = gpiozero.LED(7)

while True:
    trst.on()
    srst.off()
    time.sleep(.5)
    trst.off()
    srst.on()
    time.sleep(.5)

# Disable power
vtarget_en.off()
