import argparse
import subprocess

def dig(target):
    prefix = 'banana'
    command = 'dig +dnssec ' + prefix + '.' + target
    #wsl = windows subsystem for linux
    output = subprocess.getoutput("wsl.exe " + command)
    info = [line for line in output.strip().splitlines() if 'NSEC' in line]
    domains = set()
    for x in info:
        for temp in x.split(' '):
            if target in temp and temp not in domains:
                domains.add(temp)
    for el in domains:
        print(el)

    #[domains.add(temp) for temp in x.strip().split(' ') if 'arin.net' in temp for x in info]


def test():
    print('hi from test!')


def main():
    target = 'arin.net'
    dig(target)



    
main()
