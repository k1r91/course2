import os
import subprocess
ret = subprocess.call('ls -l', shell=True)
p = subprocess.Popen('ls -l', shell=True, stdout=subprocess.PIPE)
out = p.stdout.read()
print('out:', out)
# process to count words, line breaks and symbols
p = subprocess.Popen('wc', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# transfer string to process p
out, err = p.communicate(b'asdlkfjhreuioyert saudfiyhoeiut, \n sdifusd\n asd')
print(out)
p1 = subprocess.Popen('ls -l', shell=True, stdout=subprocess.PIPE)
p2 = subprocess.Popen('wc', shell=True, stdin=p1.stdout, stdout=subprocess.PIPE)
print(p2.stdout.read())
files = os.listdir(os.path.dirname(__file__))
with subprocess.Popen(['gzip', '-k', '-f', *files], stdout=subprocess.PIPE):
    print('Waiting for pack...')