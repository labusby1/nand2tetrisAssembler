import re
import os

def main():
	#File name is formatted properly with .asm file type
	directory = input('Enter directory location (blank for current): ')
	if directory == '':
		directory = os.getcwd()

	inFile = input('Enter text file name:')
	if inFile.endswith('.asm') == False:
		inFile = inFile + '.asm'
	inFile = directory +'/' + inFile
	#Open the file accordingly
	try:
		f = open(inFile, 'r')
	except: 
		return print('File not found!')


	#Need to create a file to write the machine code if not already existing
	#formatting output file name
	outFile = inFile.rstrip('.asm') + 'MachineCode.hack'
	g = open(outFile, 'w+')


	for line in f:
		print('Line to be read: ' + line)
		instruction = Instruction(line)
		instruction.defineType()
		instruction.convert()
		if (instruction.getConverted() != ''):
			print('Line converted to binary: '+ instructionEasyRead(instruction.getConverted()))
			g.write(str(instruction.getConverted())+ '\n')
		#delete the instruction from memory
		del instruction
	

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
		test = removeWhiteSpace(self.line)
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

			codeLine = self.line
			atIndex = codeLine.find('@')

			codeLine = codeLine[atIndex + 1:]
			intVal = int(codeLine)
			
			#An A-insturction always starts with a zero
			binaryEquate = '0'
			for i in range(14, -1, -1):
				if (intVal - 2**i >= 0):
					intVal = intVal - 2**i
					binaryEquate += '1'
				else:
					binaryEquate += '0'
			return binaryEquate
		else:
			errormsg = 'Error in converting A-instruction'
			return errormsg
	
	def convert(self):
		if self.type == 'C-instruction':
			converted = '111'
			resultingBinary = str(self.dictSearch())
			if resultingBinary == 'error':
				self.converted = ''
			else: 
				self.converted = converted + resultingBinary
			

		elif self.type == 'A-instruction':
			resultingBinary = self.findBinary()
			self.converted = resultingBinary
		else:
			self.converted = ''
			

	def dictSearch(self):
		compCases = {
			'1':'0111111',
			'-1':'0111010',
			'0':'0101010',
			'A':'0110000',
			'D':'0001100',
			'!D':'0001101',
			'!A':'0110001',
			'-D':'0001111',
			'-A':'0110011',
			'D+1':'0011111',
			'A+1':'0110111',
			'D-1':'0001110',
			'A-1':'0110010',
			'D+A':'0000010',
			'D-A':'0010011',
			'A-D':'0010011',
			'D&A':'0000000',
			'D|A':'0010101',
			'M':'1110000',
			'!M':'1110001',
			'-M':'1110011',
			'M+1':'1110111',
			'M-1':'1110010',
			'D+M':'1000010',
			'D-M':'1010011',
			'M-D':'1000111',
			'D|M':'1010101',
			'D&M':'1000000'
		}

		destCases = {
			'M':'001',
			'D':'010',
			'MD':'011',
			'A':'100',
			'AM':'101',
			'AD':'110',
			'AMD':'111'
		}

		jumpCases = {
			'JGT':'001',
			'JEQ':'010',
			'JGE':'011',
			'JLT':'100',
			'JNE':'101',
			'JLE':'110',
			'JMP':'111',
		}

		returnValue = ''

		spliceComp = str(self.getLine())
		spliceComp = removeWhiteSpace(spliceComp)
		spliceDest = spliceComp
		spliceJump = spliceComp
		destIndex = spliceComp.find('=')
		if (destIndex > -1):
			spliceComp = spliceComp[destIndex+1:]
			spliceDest = spliceDest[:destIndex]
			
		
		jumpIndex = spliceComp.find(';')
		if(jumpIndex > -1):
			spliceJump = spliceComp[jumpIndex+1:]
			spliceComp = spliceComp[:jumpIndex]
			
		if spliceComp in compCases:
			returnValue += compCases[spliceComp]

		else:
			errormsg = 'error'
			return errormsg
		
		if spliceDest in destCases:
			returnValue += destCases[spliceDest]

		else:
			returnValue += '000'

		if spliceJump in jumpCases:
			returnValue += jumpCases[spliceJump]

		else:
			returnValue += '000' 

		return returnValue

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