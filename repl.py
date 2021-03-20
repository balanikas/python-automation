import os
import threading
from datetime import datetime, timezone
import chrome_bookmarks
import requests
import IPython
from termcolor import colored
from pathlib import Path


class Activities:

    @staticmethod
    def gaming_news():
        import webbrowser
        rock = "https://www.rockpapershotgun.com/"
        webbrowser.open_new(rock)

    @staticmethod
    def zen():
        import psutil
        for proc in psutil.process_iter():
            if "Spotify" in proc.name():
                proc.kill()

    @staticmethod
    def repo_status(*args):
        # usage: repo("c:\\source")
        repo_root = args[0]

        print("repos in '{}' order by last modified".format(repo_root))

        def get_repo_modified_date():
            for dir in (os.path.join(repo_root, i) for i in os.listdir(repo_root) if
                        os.path.isdir(os.path.join(repo_root, i))):
                last_mod = max(os.stat(root).st_mtime for root, _, _ in os.walk(dir))
                modified = datetime.fromtimestamp(last_mod, tz=timezone.utc).date()

                yield (dir, str(modified))

        for i in sorted(get_repo_modified_date(), key=lambda x: x[1], reverse=True):
            print(i)

    @staticmethod
    def check_sites():

        def check_url(u):
            try:
                response = requests.get(u.url)
                print(u.url, response.status_code)
            except:
                print(colored(u.url + " FAILED", "red"))

        threads = []
        for u in chrome_bookmarks.urls:
            t = threading.Thread(target=check_url, args=(u,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    @staticmethod
    def count_lines(*args):
        # usage: count_lines('c:\\source\\ping','*.cs')
        print("counting lines of '{}' in {}".format(args[1], args[0]))
        result = list(Path(args[0]).rglob(args[1]))

        line_count = 0
        for f in result:
            try:
                with open(f, 'r') as file:
                    lines = file.readlines()
                    line_count += len(lines)
            except:
                continue

        return line_count


header = "Welcome to myspace!"
footer = "Thanks for visiting myspace, bye bye!"
scope_vars = {
    Activities.gaming_news.__name__: lambda: Activities.gaming_news(),
    Activities.zen.__name__: lambda: Activities.zen(),
    Activities.repo_status.__name__: lambda p: Activities.repo_status(p),
    Activities.check_sites.__name__: lambda: Activities.check_sites(),
    Activities.count_lines.__name__: lambda path, pattern: Activities.count_lines(path, pattern)
}

print(header)
IPython.start_ipython(argv=[], user_ns=scope_vars)
print(footer)
