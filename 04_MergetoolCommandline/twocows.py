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

    def do_exit(self, arg):
        """Выйти из CowShell."""
        print("До свидания!")
        return True

if __name__ == "__main__":
    CowShell().cmdloop()