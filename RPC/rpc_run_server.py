from rpc_server import RPCServer


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


server = RPCServer()

server.registerMethod(add)
server.registerMethod(sub)

server.run()
