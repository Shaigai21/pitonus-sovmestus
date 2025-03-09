import cmd
import shlex
import cowsay

class CowShell(cmd.Cmd):
    intro = "Добро пожаловать в CowShell! Введите help для списка команд."
    prompt = "twocows> "

    def do_list_cows(self, arg):
        """Список доступных коров."""
        print("Доступные коровы:", ", ".join(cowsay.list_cows()))

    def do_make_bubble(self, arg):
        """Создать пузырь с текстом.
        Использование: make_bubble <текст> [wrap_text=True] [brackets=cowsay.THOUGHT_OPTIONS]
        """
        args = shlex.split(arg)
        if not args:
            print("Ошибка: Необходимо указать текст.")
            return
        text = args[0]
        kwargs = {}
        if len(args) > 1:
            for a in args[1:]:
                if "=" in a:
                    key, value = a.split("=", 1)
                    kwargs[key] = eval(value)
        print(cowsay.make_bubble(text, **kwargs))

    def do_cowsay(self, arg):
        """Корова говорит.
        Использование: cowsay <сообщение1> [корова1 [параметр=значение...]] reply <сообщение2> [корова2 [параметр=значение...]]
        Пример: cowsay "Hi there" moose eyes="^^" reply "Ahoy!" sheep
        """
        args = shlex.split(arg)
        if not args:
            print("Ошибка: Необходимо указать сообщение.")
            return

        try:
            reply_index = args.index("reply")
        except ValueError:
            print("Ошибка: Необходимо указать 'reply' для второй коровы.")
            return

        message1 = args[0]
        cow1 = args[1] if reply_index != 1 else "default"
        kwargs1 = {}
        for a in args[2:reply_index]:
            if "=" in a:
                key, value = a.split("=", 1)
                kwargs1[key] = value

        message2 = args[reply_index + 1]
        cow2 = args[reply_index + 2] if len(args) > reply_index + 2 else "default"
        kwargs2 = {}
        for a in args[reply_index + 3:]:
            if "=" in a:
                key, value = a.split("=", 1)
                kwargs2[key] = value
        cow1_lines = cowsay.cowsay(message=message1, cow=cow1, **kwargs1).split("\n")
        cow2_lines = cowsay.cowsay(message=message2, cow=cow2, **kwargs2).split("\n")

        max_len = max(len(cow1_lines), len(cow2_lines))
        cow1_lines = [""] * (max_len - len(cow1_lines)) + cow1_lines
        cow2_lines = [""] * (max_len - len(cow2_lines)) + cow2_lines

        width = max(len(line) for line in cow1_lines)

        combined = []
        for line1, line2 in zip(cow1_lines, cow2_lines):
            combined.append(line1.ljust(width) + line2)
        print("\n".join(combined))

    def complete_cowsay(self, text, line, begidx, endidx):
        """Автодополнение для команды cowsay."""
        args = shlex.split(line[:begidx])
        if not args or len(args) == 1:
            return []
        try:
            if args.index("reply") + 1 == len(args):
                return []
        except ValueError:
            pass

        if args[-1] in cowsay.list_cows() or "=" in args[-1]:
            return []
        return [cow for cow in cowsay.list_cows() if cow.startswith(text)]

    def do_cowthink(self, arg):
        """Корова думает.
        Использование: cowthink <сообщение> [[название] [параметр=значение...]]
        """

        args = shlex.split(arg)
        if not args:
            print("Ошибка: Необходимо указать сообщение.")
            return
        message = args[0]
        cow = "default"
        kwargs = {}
        if len(args) > 1:
            cow = args[1]
        if len(args) > 2:
            for a in args[2:]:
                if "=" in a:
                    key, value = a.split("=", 1)
                    kwargs[key] = value
        print(cowsay.cowthink(message, cow=cow, **kwargs))

    def complete_cowthink(self, text, line, begidx, endidx):
        """Автодополнение для команды cowthink."""
        args = shlex.split(line[:begidx])
        if not args or len(args) == 1:
            return []

        if args[-1] in cowsay.list_cows() or "=" in args[-1]:
            return []
        return [cow for cow in cowsay.list_cows() if cow.startswith(text)]

    def do_exit(self, arg):
        """Выйти из CowShell."""
        print("До свидания!")
        return True

if __name__ == "__main__":
    CowShell().cmdloop()