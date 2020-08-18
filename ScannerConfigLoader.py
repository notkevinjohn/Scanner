import xml.etree.ElementTree as ET
import sys

class ScannerConfigLoader():
	def __init__(self, configFile):
		self.config = {}
		tree = ET.parse(configFile)
		root = tree.getroot()

		for child in root:
			if child.tag == "Channels":
				self.config['Channels'] = []
				for element in child:
					self.config['Channels'].append(element.text)



if __name__ == "__main__":
	config = sys.argv[1]
	scannerLoader = ScannerConfigLoader(config)
	print (scannerLoader.config)
