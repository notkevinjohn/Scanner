#! /usr/bin/python3

from Controllers.APControl import APControl
from Controllers.OutputManager import OutputManager
from ScannerConfigLoader import ScannerConfigLoader
from termcolor import colored
import time
import datetime

class Scanner():
	def __init__(self):
		self.output = OutputManager()
		self.output.printStatus("Starting Scanner")
		self.configLoader = ScannerConfigLoader("config.xml")
		self.config = self.configLoader.config
		channels = ", ".join(self.config['Channels'])
		self.output.printStatus("Scanning Channels "+channels)
		self.apControl = APControl(int(self.config['Channels'][0]), 'apeg792', self)
		dateTime = datetime.datetime.now()
		dateString = dateTime.strftime("%d-%m-%y_%H:%M")
		self.logFile = "logs/ScanLog_"+dateString
		self.output.printStatus(self.logFile)

	def scan(self):
		self.apControl.start()
		self.batch = self.apControl.batch
		self.apControl.setDiscover(True)

		for channel in self.config['Channels']:
			self.apControl.setChannel(int(channel))
			self.output.printStatus("Scanning Channel "+channel)
			self.batch.Discovery.discoverAll(60)
			self.awaitOperation()

			with open(self.logFile, "a+") as log:
				for serial in self.batch.Discovery.discovered:
					log.write(channel+", "+serial+"\n")
					print (channel, serial)


	def awaitOperation(self):
		while self.batch.complete == False:
			time.sleep(1)
			self.output.printProcess(self.batch.Message)
		self.output.printProcess(self.batch.Message, True)

	def end(self):
		self.apControl.stop()

if __name__ == "__main__":
	scanner = Scanner()
	scanner.scan()
	scanner.end()

