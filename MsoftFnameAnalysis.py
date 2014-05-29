# -*- coding: utf-8 -*-
# based on: http://msdn.microsoft.com/en-us/library/aa365247(VS.85).aspx

class MsoftFnameAnalysis:

	report = ''

	def completeFnameAnalysis(self, s):
		self.detectNonAsciiCharacters(s)
		self.detectNonRecommendedCharacters(s)
		self.detectNonPrintableCharacters(s)
		self.detectMsoftReservedNames(s)
		self.detectSpaceAtEndOfName(s)
		self.detectPeriodAtEndOfName(s)

	def detectNonAsciiCharacters(self, s):
		#Nicer method: all(ord(c) < 128 for c in s)
		nonascii = False
		char = ''
		for c in s:
			if ord(c) > 128:
				nonascii = True
				char = c
				break
		if nonascii == True:
			self.reportIssue(s, "contains, characters outside of ASCII range:", hex(ord(char)))

	def detectNonRecommendedCharacters(self, s):
		charlist = ['<','>',':','"','/','\\','?','*','|', ']', '[']
		for c in charlist:
			if c in s:
				self.reportIssue(s, "contains, non-recommended character:", hex(ord(c)))
				break

	def detectNonPrintableCharacters(self, s):
		for c in range(0x1f):
			if chr(c) in s:
				self.reportIssue(s, "contains, non-printable character:", hex(c))
				break

	def detectMsoftReservedNames(self, s):
		badnames = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', \
							'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', \
								'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', \
									'LPT6', 'LPT7', 'LPT8', 'LPT9']
				
		for c in badnames:
			if c.lower() in s[0:len(c)].lower():
				problem = True
				try:
					if s[len(c)] == '.':					#zero-based index
						problem = True
					else:
						problem = False
				except IndexError:
					problem = True
				if problem == True:
					self.reportIssue(s, "contains, reserved name:", c)

	def detectSpaceAtEndOfName(self, s):
		if s.endswith(' '):
			self.reportIssue(s, "has a space as its last character.")
			
	def detectPeriodAtEndOfName(self, s):		
		if s.endswith('.'):
			self.reportIssue(s, "has a period as its last character.")
	
	def reportIssue(self, s, msg, value=''):
		self.report = "File: " + s + " " + msg + " " + value
		print self.report
	
	def __detect_invalid_characters_test__(self):
		#Strings for unit tests
		test_strings = ['COM4', 'COM4.txt', '.com4', 'abcCOM4text', 'abc.com4.txt.abc', 'con', 'CON', 'consumer', 'space ', 'preiod.', '�', '�', '�', '���', 'file[bracket]one.txt', 'file[two.txt', 'filethree].txt', '-=_|\"', '(<|>|:|"|/|\\|\?|\*|\||\x00-\x1f)']	
	
		# First test, all ASCII characters?
		for s in test_strings:
			self.detect_invalid_characters(s)