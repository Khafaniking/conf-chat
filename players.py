import zmq
import sys
import threading

player_port = int(sys.argv[1])
player_name = sys.argv[2]

context = zmq.Context()

#pub
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(f"tcp://*:{player_port}")

#sub
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:5556")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

rep_socket = context.socket(zmq.REP)
rep_socket.bind(f"tcp://*:{player_port + 1000}")

current_input = ""


# public chat
def listen_public_chat():
    while True:
        message = sub_socket.recv_string()
        if not message.startswith(player_name):  # skip self-sent messages
            sys.stdout.write("\r\033[K")
            print(f"\n[Public Chat] {message}")
            sys.stdout.write(f"{player_name}, enter command (/dm, /public): {current_input}")
            sys.stdout.flush()



def listen_dm():
    while True:
        message = rep_socket.recv_string()
        sys.stdout.write("\r\033[K")  # Clear the line
        print(f"\n[DM from {message.split(':')[0]}] {message.split(':')[1]}")
        rep_socket.send_string("Message received!")  # Send acknowledgment

        #sys.stdout.write(f"{player_name}, enter command (/dm, /public): ")
        #removed cause was creating issues with the user prompts
        sys.stdout.flush()

#/dm, /public, past iterations had /group, /joingroup
def command_handler():
    global current_input

    while True:
        current_input = ""
        command = input(f"{player_name}, enter command (/dm, /public): ").strip()

        if command == "/dm":
            target_port = input("Enter the target player's port to DM: ").strip()
            dm_socket = context.socket(zmq.REQ)
            dm_socket.connect(f"tcp://localhost:{int(target_port) + 1000}")

            while True:
                current_input = input("DM > ").strip()
                if current_input == "/back":
                    break
                if current_input:
                    dm_socket.send_string(f"{player_name}: {current_input}")
                    ack = dm_socket.recv_string()
                    print(f"[DM acknowledgment] {ack}")

        elif command == "/public":
            while True:
                current_input = input(f"{player_name}, type your message: ").strip()
                if current_input == "/back":
                    break
                if current_input:
                    pub_socket.send_string(f"{player_name}: {current_input}")

threading.Thread(target=listen_public_chat, daemon=True).start()
threading.Thread(target=listen_dm, daemon=True).start()

command_handler()










