import argparse
import subprocess
import platform
import sys

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","-D", help="enter -d followed by domain", type=str)
    args = parser.parse_args()  # get args
    output = []
    if args.d is not None:
        output.append(args.d)
    else:
        print('Domain not specified exiting program!')
        sys.exit(-1)
    return output

"""
Helper function to test if host is reachable or not
@param url 
@return True or False depending if url is pingable
"""
def pingOk(host):
    output = subprocess.getoutput("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host))
    print(output)
    for line in output.splitlines():
        if 'Request timed out' in line or 'Ping request could not find host':
            return False
    return True


def mailServers(url):
    command = f'dig {url} MX'
    pass

def dig(target):
    prefix = 'apple'
    command = 'dig +dnssec ' + prefix + '.' + target
    #wsl = windows subsystem for linux
    output = subprocess.getoutput("wsl.exe " + command)
    info = []
    NSEC3_flag = False
    for line in output.strip().splitlines():
        if 'NSEC' in line:
            info.append(line)
        elif 'NSEC3' in line:
            NSEC3_flag = True
            info.append(line)
        else:
            continue
    domains = set()
    for x in info:
        for temp in x.split(' '):
            temp = temp[:len(temp)-1]
            if target in temp and temp not in domains and temp != target:
                domains.add(temp.replace(' ',''))
    for el in domains:
        print(el)

    #replace all numbers with spaces as well as replace IN AND NSEC
    #[domains.add(temp) for temp in x.strip().split(' ') if 'arin.net' in temp for x in info]

def main():
    args = parseArgs()
    domain = args[0]
    print(domain)

if __name__ == '__main__':
    main()
