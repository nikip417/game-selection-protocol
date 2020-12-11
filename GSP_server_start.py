from server.GSP_server import GSPServer

def main():
	"""
	Start up GSP server script
	"""
	gsp_server = GSPServer()
	gsp_server.start()

if __name__ == "__main__":
	main()
