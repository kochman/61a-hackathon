import os
import stem.process
import tempfile

from server import app

class ChatHiddenService():

	def __init__(self):
		self.hidden_service_dir = tempfile.TemporaryDirectory()
		self.tor_process = stem.process.launch_tor_with_config(
			config = {
				'HiddenServiceDir': self.hidden_service_dir.name,
				'HiddenServicePort': '80 127.0.0.1:9999'
			},
			take_ownership = True
		)
		with self.hidden_service_dir as h:
			with open(os.path.join(h, 'hostname'), 'r') as f:
				self.onion_address = f.read().strip()
		print('Tor hidden service address: {}'.format(self.onion_address))

if __name__ == '__main__':
	hs = ChatHiddenService()
	print('Go to http://{} to chat'.format(hs.onion_address))
	print()
	app.run(host='127.0.0.1', port=9999, debug=False)
