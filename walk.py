import subprocess
import platform
import sys

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


def check_args():
    if len(sys.argv) != 2:
        print('Incorrect number of arguments, exiting program')
        print('Run as python3 name_of_domain')
        sys.exit(-1)


def dig(target, prefix, NSEC3_flag, domains, counter):
    if counter > 4 or ('z' in prefix or 'z' == prefix):
        return domains, NSEC3_flag
    else:
        url = prefix + '.' + target
        if pingOk(url): url = str((prefix * 4)) + '.' + target
        command = 'dig +dnssec ' + url
        # wsl = windows subsystem for linux
        output = subprocess.getoutput("wsl.exe " + command)
        info = []
        for line in output.strip().splitlines():
            if 'NSEC' in line:
                info.append(line)
            elif 'NSEC3' in line:
                NSEC3_flag = True
                info.append(line)
            elif target in line:
                info.append(line)
            else:
                continue

        for line in info:
            words = line.replace('\t', ' ').split(' ')
            for word in words:
                word = word[:len(word) - 1].replace(' ', '').replace(';', '')
                if target in word:
                    print('word is: ', word)
                if len(word) < len(target):
                    continue
                if word in domains:
                    counter += 1
                    continue
                if len(word) == 55 and NSEC3_flag is True:  # indicates it's hashed
                    domains.add(word)
                    continue
                if target in word and word not in domains and word != url:
                    domains.add(word)

        """tmp = sorted(list(domains))
        for domain in tmp:
            if domain[0] == prefix:
                prefix = chr(ord(domain[0]) + 1)  # shift letter by 1
                break
    
        if len(tmp) >= 1:
            if prefix == tmp[0][0]:
                prefix = chr(ord(prefix) + 1)"""
        prefix = chr(ord(prefix) + 1)  # shift letter by 1
        return dig(target, prefix, NSEC3_flag, domains, counter)


def pretty_print(domains, NSEC3_flag):
    print('[*] Printing Results')
    if NSEC3_flag is True:
        print('\t Domain is using NSEC3 use other tool to crack hashes')
    for domain in sorted(list(domains)):
        print('\t ' + str(domain))


def main():
    check_args()
    domain = sys.argv[1]
    info = dig(domain, prefix='a', NSEC3_flag=False, domains=set(), counter=0)
    print('Info is: ', info)
    domains = info[0]
    NSEC3_flag = info[1]
    pretty_print(domains, NSEC3_flag)


if __name__ == '__main__':
    main()
