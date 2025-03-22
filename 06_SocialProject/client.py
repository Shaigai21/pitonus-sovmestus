import cmd
import socket
import threading
import readline

class CowChatClient(cmd.Cmd):
    prompt = 'cowchat> '

    def __init__(self, host='localhost', port=1337):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.cow_names = set()
        self.users = set()
        self.me = None

        self._recv_initial_message()

        self.update_cow_names()
        self.update_users()

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def _recv_initial_message(self):
        """Чтение начального сообщения от сервера после подключения."""
        initial_message = self.socket.recv(1024).decode().strip()
        if initial_message:
            print(initial_message)

    def update_cow_names(self):
        self.socket.sendall(b'cows\n')
        response = self.socket.recv(1024).decode().strip()
        if response.startswith('Available cow names: '):
            self.cow_names = set(response.split(': ')[1].split(', '))

    def update_users(self):
        self.socket.sendall(b'who\n')
        response = self.socket.recv(1024).decode().strip()
        if response.startswith('Registered users: '):
            self.users = set(response.split(': ')[1].split(', '))

    def receive_messages(self):
        """Функция для чтения сообщений от сервера в фоновом режиме."""
        while True:
            try:
                response = self.socket.recv(1024).decode().strip()
                if response:
                    if response.startswith('Logged in as'):
                        self.me = response[13:]
                        self.update_users()
                    print(f"\n{response}\n{self.prompt}{readline.get_line_buffer()}", end="", flush=True)
            except ConnectionResetError:
                print("\nConnection to the server was lost.")
                break

    def do_login(self, arg):
        """Login to the chat using a cow name: login <cow_name>"""
        if not arg:
            print("Usage: login <cow_name>")
            return
        self.socket.sendall(f'login {arg}\n'.encode())

    def complete_login(self, text, line, begidx, endidx):
        if not text:
            return list(self.cow_names)
        return [cow for cow in self.cow_names if cow.startswith(text)]

    def do_say(self, arg):
        """Send a message to a user: say <user> <message>"""
        if not self.me:
            print("Login to send and receive messages.")
            return
        args = arg.split()
        if len(args) < 2:
            print("Usage: say <user> <message>")
            return
        target, message = args[0], ' '.join(args[1:])
        self.socket.sendall(f'say {target} {message}\n'.encode())

    def complete_say(self, text, line, begidx, endidx):
        if not text:
            return list(self.users)
        return [user for user in self.users if user.startswith(text)]

    def do_yield(self, arg):
        """Broadcast a message to all users: yield <message>"""
        if not self.me:
            print("Login to send and receive messages.")
            return
        if not arg:
            print("Usage: yield <message>")
            return
        self.socket.sendall(f'yield {arg}\n'.encode())

    def do_quit(self, arg):
        """Quit the chat: quit"""
        self.socket.sendall(b'quit\n')
        print("Goodbye!")
        return True

    def do_who(self, arg):
        """List registered users: who"""
        self.socket.sendall(b'who\n')

    def do_cows(self, arg):
        """List available cow names: cows"""
        self.socket.sendall(b'cows\n')

    def do_EOF(self, arg):
        """Exit the chat: Ctrl+D"""
        print("Goodbye!")
        return True

    def emptyline(self):
        pass

if __name__ == '__main__':
    client = CowChatClient()
    client.cmdloop()