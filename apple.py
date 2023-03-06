import subprocess
MyWish = subprocess.run(
    ['netsh', 'interface', 'set', 'interface', "wi-fi", "ENABLED"])
MyWish
