from rpc_client import RPCClient

server = RPCClient()

server.connect()

print(server.add(5, 6))
print(server.sub(5, 6))

server.disconnect()
