import zmq

context = zmq.Context()

# SUB
sub_socket = context.socket(zmq.SUB)
player_ports = [5551, 5552, 5553, 5554, 5555]
for port in player_ports:
    sub_socket.connect(f"tcp://localhost:{port}")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

# PUB
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

print("PublicChat is running on port 5556, listening to player ports 5551-5555...")

while True:
    message = sub_socket.recv_string()
    if message.strip():
        print(f"\n[Public Chat] {message}")
        pub_socket.send_string(message) #share messages with all other players




