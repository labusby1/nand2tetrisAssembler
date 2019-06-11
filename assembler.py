from unittest.mock import patch
from unittest import TestCase

def main():
	#File name is formatted propperly
	inFile = input('Enter text file name:')
	if inFile.endswith('.txt') == False:
		inFile = inFile + '.txt'

	#Open the file accordingly
	try:
		f = open(inFile, 'r')
		contents = f.read()
	except: 
		print('File not found!')

	f = open(inFile, 'r')
	#Need to create a file to write the machine code if not already existing
	#formatting output file name
	outFile = inFile.rstrip('.txt') + 'MachineCode.txt'
	g = open(outFile, 'w+')



	#First we decide wether the line is an A or C instruction
	#for line in 
	line1 = f.readline()
	print('Line to be read: ')
	
	instruction1 = Instruction(line1)
	print(instruction1.getLine())
	#We'll test for the type outside the class since we can then skip the rest if
	#type is a comment.
	instruction1.defineType()
	print('instruction type: ' + instruction1.getType())
	

	#Next we can convert the isntruction into machine code
	if instruction1.type == 'A-instruction':
		instruction1.findBinary()
		print(instructionEasyRead(instruction1.getConverted()))
		#print(binaryVal)
	elif instruction1.type == 'C-instruction':
		instruction1.convert()

	print('Converted: ' + instruction1.getConverted())

	#Closing the files
	f.close()
	g.close()


class Instruction:
	def __init__(self, line):
		self.type = 'undefined'
		self.jump = False
		self.dest = False
		self.line = line
		self.converted = ''

		#Dealing with white spaces 
		self.line = removeWhiteSpace(self.line)

	def defineType(self):
		test = self.line
		if (test.startswith('//') or test.startswith('(')):
			self.type = 'Comment'
		elif test.startswith('@'):
			self.type = 'A-instruction'
		else:
			self.type = 'C-instruction'
		if not (test.find('=') == -1):
			self.dest = True
		if not (test.find(';') == -1):
			self.jump = True

	def findBinary(self):
		
		if self.type == 'A-instruction':
			#Here we remove the '@' symbol found before an a-instruction
			#leaving hopefully an integer value (intVal)
			intVal = self.line[1:]
			intVal = int(intVal)
			#An A-insturction always starts with a zero
			binaryEquate = '0'
			for i in range(14, -1, -1):
				if (intVal - 2**i >= 0):
					intVal = intVal - 2**i
					binaryEquate += '1'
				else:
					binaryEquate += '0'
			self.converted = binaryEquate
			return binaryEquate
		else:
			errormsg = 'Error in converting A-instruction'
			return errormsg
	
	def convert(self):
		if self.type == 'C-instruction':
			converted = '111'
			resultingBinary = self.dictSearch()
			converted = converted+str(resultingBinary)
			#print(instructionEasyRead(converted))

		else:
			errormsg = 'Error in converting C-instruction'

	def dictSearch(self):
		compCases = {
				'1':'111111',
				'-1':'111010',
				'0':'101010',
				'A':'110000',
				'D':'001100',
				'!D':'001101',
				'!A':'110001',
				'-D':'001111',
				'-A':'110011',
				'D+1':'011111',
				'A+1':'110111',
				'D-1':'001110',
				'A-1':'110010',
				'D+A':'000010',
				'D-A':'010011',
				'A-D':'010011',
				'D&A':'000000',
				'D|A':'010101',
				'M':'110000',
				'!M':'110001',
				'-M':'110011',
				'M+1':'110111',
				'M-1':'110010',
				'D+M':'000010',
				'D-M':'010011',
				'M-D':'000111',
				'D|M':'010101'
			}

		spliceThis = str(self.getLine())
		destIndex = spliceThis.find('=')
		if (destIndex > -1):
			spliceThis = spliceThis[destIndex+1:]
		
		
		jumpIndex = spliceThis.find(';')
		if(jumpIndex > -1):
			spliceThis = spliceThis[:jumpIndex]


		#Need to remove any whitespaces which might interfer with dictionary search
		#Since i plan only to do this 
		spliceThis = "".join(spliceThis.split())
		if spliceThis in compCases:
			self.converted = compCases[spliceThis]
			return compCases[spliceThis]

		else:
			errormsg = 'error'
			return errormsg
	

	

	def getLine(self):
		return self.line

	def getType(self):
		return self.type

	def getConverted(self):
		return self.converted


def removeWhiteSpace(string):
		string = "".join(string.split())
		return string	

def instructionEasyRead(string):
	easyRead = string
	j = 0
	for i in range(4, len(string), 4):
		i = i+j
		easyRead = easyRead[:i] + ' ' + easyRead[i:]
		j += 1
	return easyRead
main()