import subprocess
p_list = []

while True:
    user = input('Run 10 clients simultaneously? (s) / close clients(x) / exit app (q)')
    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            p_list.append(subprocess.Popen('python3 socket_server_time_client.py',
                                           shell=True))
        print('10 clients ran')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()