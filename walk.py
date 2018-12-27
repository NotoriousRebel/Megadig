import argparse
import subprocess
import platform
import sys

"""
    A simple program to recursively walk zone files for domains that utilize NSEC
"""


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "-D", help="enter -d followed by domain", type=str)
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
    output = subprocess.getoutput("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', host))
    for line in output.splitlines():
        if 'Request timed out' in line or 'Ping request could not find host' in line:
            return False
    return True


def mailServers(url):
    command = f'dig {url} MX'
    pass


def dig(target, prefix, NSEC3_flag, domains, stop_flag):
    if stop_flag:
        return sorted(list(domains)), NSEC3_flag
    else:
        command = 'dig +dnssec ' + prefix + '.' + target
        # wsl = windows subsystem for linux
        output = subprocess.getoutput("wsl.exe " + command)
        info = []
        NSEC3_flag = False
        for line in output.strip().splitlines():
            if 'NSEC' in line:
                info.append(line)
            elif 'NSEC3' in line:
                NSEC3_flag = True
                info.append(line)
            elif target in line and target != (prefix + '.' + target):
                info.append(line)
            else:
                continue

        domains = set()
        for line in info:
            print('line: ', line)
            words = line.replace('\t', ' ').split(' ')
            for word in words:
                word = word[:len(word) - 1]
                if target in word and word not in domains and word != target:
                    domains.add(word.replace(' ', '').replace(';', ''))

        start = ''
        tmp = sorted(list(domains))
        for i in range(len(tmp)):
            domain = tmp[i]
            if domain[0] == prefix:
                prefix = chr(ord(domain[0]) + 1)  # shift letter by 1
        if prefix == 'z': stop_flag = True
        dig(target, prefix, NSEC3_flag, domains, stop_flag)


def main():
    args = parseArgs()
    domain = args[0]
    info = dig(domain, prefix='a', NSEC3_flag=False, domains=set(), stop_flag=False)
    domains = info[0]
    NSEC3_flag = info[1]


if __name__ == '__main__':
    main()
