import random
import array

class generatePassword:
	def __init__(self) -> None:
		self.DEFAULT_LEN = 24
		self.DIGITS = [str(i) for i in range(10)]
		self.LOCASE_CHARACTERS = [chr(97+i) for i in range(26)]
		self.UPCASE_CHARACTERS = [chr(65+i) for i in range(26)]
		self.DEFAULT_SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<']

	def generate(self, symbols = None, length = None) -> str:
		if length != None:
			LEN = length
		else:
			LEN = self.DEFAULT_LEN
		
		if symbols != None:
			SYMBOLS = symbols
		else:
			SYMBOLS = self.DEFAULT_SYMBOLS
		COMBINED_LIST = self.DIGITS + self.UPCASE_CHARACTERS + self.LOCASE_CHARACTERS + SYMBOLS
		
		rand_digit = random.choice(self.DIGITS)
		rand_upper = random.choice(self.UPCASE_CHARACTERS)
		rand_lower = random.choice(self.LOCASE_CHARACTERS)
		rand_symbol = random.choice(SYMBOLS)
		temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
		for x in range(LEN - 4):
			temp_pass = temp_pass + random.choice(COMBINED_LIST)
		temp_pass_list = array.array('u', temp_pass)
		random.shuffle(temp_pass_list)
		
		password = ""
		for x in temp_pass_list:
			password = password + x
		
		return password

if __name__ == "__main__":
	gen = generatePassword()
	print(gen.generate())
	
	sym = ["@", "#", "$"]
	print(gen.generate(symbols=sym))

	print(gen.generate(length=20))

	print(gen.generate(symbols=sym, length=20))