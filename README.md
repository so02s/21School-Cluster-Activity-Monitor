# 21School-Cluster-Activity-Monitor
### Description
In order to visualize clusters computers accesibility for students and make finding a coding place for oneself easier, School 21's Lab Manager Freimor (Ricky in School 21) came up with the idea of autonomous Cluster Activity Monitor.
It should be set up on each of the School's floors. We've managed to set it up on the 2nd floor.
Monitor has a map embedded in its graphics. It lights up LEDs, showing which Mac seats are occupied, which are free to use and other types of seat status. It's connected to a local network and pulls data from the metrics data-point server. 
* Monitor shows seats that are either taken, free, covid-free or used for exam.
* It also lights up the viewer's position on the map.
* Brightness of the LED is dependant on ambient light level, due to embedded light sensor.
* It should potentially support extra add-ons.

<img src="https://user-images.githubusercontent.com/21167984/194581257-6767a5d4-8eba-4e4f-b2fb-2148377a2d4b.png" width="1000">

### Monitor consists of:
* 5 front PCB's which we call "modules", with school claster names (Atrium, Illusion, Oasis, Atlantis and Mirage)
  * ~450 SK9822 2020 leds
  * STM32F030* microcontroller
* 1 "motherboard" PCB
  * Raspberry Pi Zero W
  * ADS1115 for photoresistor
* Mean Well IRM-60-5ST power supply
* 3D printed skeleton structure
  * M1.2 inserted nuts and bolts for fixing modules in 3d printed front layer
  * M4 inserted nuts and bolts for fixing front layer to skeleton main body
  * 4 wall plug for fixing main body to wall
* Front PCB's shield made of polycarbonate sheet

<img src="https://user-images.githubusercontent.com/21167984/194715495-54764cdb-93ce-4289-a609-c471bc68dd42.png" width="1000">

Done by team: Ricky, Bomanyte.
