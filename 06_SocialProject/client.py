import cmd
import socket
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

    def do_login(self, arg):
        """Login to the chat using a cow name: login <cow_name>"""
        if not arg:
            print("Usage: login <cow_name>")
            return
        self.socket.sendall(f'login {arg}\n'.encode())
        response = self.socket.recv(1024).decode().strip()
        print(response)
        if response.startswith('Logged in as'):
            self.me = arg
            self.update_users()

    def complete_login(self, text, line, begidx, endidx):
        if not text:
            return list(self.cow_names)
        return [cow for cow in self.cow_names if cow.startswith(text)]

    def do_quit(self, arg):
        """Quit the chat: quit"""
        self.socket.sendall(b'quit\n')
        print("Goodbye!")
        return True

    def do_who(self, arg):
        """List registered users: who"""
        self.socket.sendall(b'who\n')
        response = self.socket.recv(1024).decode().strip()
        print(response)

    def do_cows(self, arg):
        """List available cow names: cows"""
        self.socket.sendall(b'cows\n')
        response = self.socket.recv(1024).decode().strip()
        print(response)

    def do_EOF(self, arg):
        """Exit the chat: Ctrl+D"""
        print("Goodbye!")
        return True

    def emptyline(self):
        pass

if __name__ == '__main__':
    client = CowChatClient()
    client.cmdloop()