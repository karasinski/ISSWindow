#!/bin/bash
while true
do
	#ISS Stream
	livestreamer http://ustream.tv/channel/iss-hdev-payload best --player omxplayer --fifo
	#Osprey Stream
	#livestreamer http://ustream.tv/exploreOsprey best --player omxplayer --fifo
	#Random stream
	#livestreamer http://ustream.tv/siliconangle best --player omxplayer --fifo
done