# Production test

Script to test that all features of the JTAG-Hat are functional

Required material:

* Raspberry Pi w/patched OpenOCD
* JTAG_Hat (DUT)
* STM32F103RC development board, or board with similar processor that supports both JTAG and SWD programming interfaces
* 2x LED + ~330 ohm resistor, connected in series. Attach one between 3.3V and SRST on the development board, and the other between 3.3V and TRST on the develoment board.
* 10-pin, 1.27mm ribbon cable
* 20-pin 2.54mm ribbon cable
* 20-pin to 10-pin adapter board (if development board only has 20-pin interface)
* 2-pin, 2.54mm jumper

Steps:

1. Boot the raspberry pi
2. Plug a JTAG Hat into the raspberry pi
3. Connect the 2-pin jumper between TX and RX on the UART header
4. Connect the development board to the JTAG_Hat using the 20 pin ribbon cable
5. Run the test script. All 8 tests should pass
6. Observe the reset LEDs. they should flash in an alternating pattern
7. Press Ctrl+C to stop the test program
8. Remove the 20 pin ribbon cable
9. Connect the development board to the JTAG_Hat using the 10 pin ribbon cable
10. Run the test script again. All 8 tests should pass again
11. Observe the reset LEDs. Only the one connected to SRST should be flashing
12. Press Ctrl+C to stop the test program
13. Remove the JTAG_Hat; repeat steps with next JTAG_Hat
