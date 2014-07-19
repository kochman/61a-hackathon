import argparse
import os
import shallot
import stem.process
import tempfile

from server import app

class ChatHiddenService():

	def __init__(self, key=None):
		self.hidden_service_dir = tempfile.TemporaryDirectory()
		if key:
			self.key = key
			with open(os.path.join(self.hidden_service_dir.name, 'private_key'), 'w') as f:
				f.write(self.key)

		self.tor_process = stem.process.launch_tor_with_config(
			config = {
				'HiddenServiceDir': self.hidden_service_dir.name,
				'HiddenServicePort': '80 127.0.0.1:9999'
			},
			take_ownership = True
		)
		with open(os.path.join(self.hidden_service_dir.name, 'hostname'), 'r') as f:
			self.onion_address = f.read().strip()
		print('Tor hidden service address: {}'.format(self.onion_address))

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--prefix', type=str, help='optional prefix for onion address', default=None)
	args = parser.parse_args()

	if args.prefix:
		print('Generating key with onion key prefix "{}"...'.format(args.prefix))
		if len(args.prefix) > 5:
			print('  Your prefix is long. Consider shortening it to speed this up.')
		shal = shallot.Shallot()
		key = shal.create_key(args.prefix)
		hs = ChatHiddenService(key)
	else:
		hs = ChatHiddenService()
	print('Go to http://{} to chat'.format(hs.onion_address))
	print()
	app.run(host='127.0.0.1', port=9999, debug=False)
