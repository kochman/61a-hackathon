import subprocess

class Shallot:
	"""Python interface for https://github.com/katmagic/Shallot"""

	def create_key(self, prefix):
		exp = '^' + prefix
		output = subprocess.check_output(['./shallot', exp]).decode()
		index = output.find('-----BEGIN RSA PRIVATE KEY-----')
		output = output[index:].strip()
		return output