import subprocess
import platform
import sys


def pingOk(host: str):
    """
    Helper function to test if host is reachable or not
    :param host host to check
    :return True or False depending if url is pingable
    """
    output = subprocess.getoutput("ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', host))
    for line in output.splitlines():
        if 'Request timed out' in line or 'Ping request could not find host' in line:
            return False
    return True


def check_args():
    """
    Helper function to check cmd args
    """
    if len(sys.argv) != 2:
        print('Incorrect number of arguments, exiting program')
        print('Run as python3 name_of_domain')
        sys.exit(-1)


def dig(target: str, prefix: chr, NSEC3_flag: bool, domains: set, counter: int) -> tuple:
    """
    Recursive function to dig target and gather urls
    :param target: target to be dig
    :param prefix: current prefix
    :param NSEC3_flag: flag to indicate if target uses NSEC3
    :param domains: set of domains
    :param counter: counter to keep track of duplicates
    :return: tuple of domains and NSEC3_flag
    """
    if counter > 6 or ('z' in prefix or 'z' == prefix):
        return domains, NSEC3_flag
    else:
        url = prefix + '.' + target
        if pingOk(url):  # check if current url is pingable and if it is make it not
            url = str((prefix * 15)) + '.' + target
        command = 'dig +dnssec ' + url
        # wsl = windows subsystem for linux
        output = subprocess.getoutput("wsl.exe " + command)  # get output to parse
        info = []
        for line in output.strip().splitlines():
            if 'NSEC' in line:
                info.append(line)
            elif 'NSEC3' in line:  # indicates urls are going to be hashed
                NSEC3_flag = True
                info.append(line)
            elif target in line:
                info.append(line)
            else:
                continue

        for line in info:
            words = line.replace('\t', ' ').split(' ')
            for word in words:
                word = word[:len(word) - 1].replace(' ', '').replace(';', '')  # strip spaces and semicolons
                if len(word) < len(target):
                    continue
                if word in domains:  # indicates we have hit a duplicate
                    counter += 1
                    continue
                if len(word) == 55 and NSEC3_flag is True:  # indicates it's hashed
                    domains.add(word)
                    continue
                if target in word and word not in domains and word != url:
                    domains.add(word)
        prefix = chr(ord(prefix) + 1)  # shift letter by 1
        return dig(target, prefix, NSEC3_flag, domains, counter)


def pretty_print(domains: set, NSEC3_flag: bool):
    """
    Function to pretty print domains
    :param domains: set of domains
    :param NSEC3_flag: flag to indicate if target uses NSEC3
    :return:
    """
    print('[*] Printing Results\n')
    if NSEC3_flag is True:
        print('\t Domain is using NSEC3 use other tool to crack hashes')
    for domain in sorted(list(domains)):  # sort and print the fruits of dig
        print("    " + str(domain))


def main():
    """
    Main function that handles logic
    """
    check_args()
    domain = sys.argv[1]
    info = dig(domain, prefix='a', NSEC3_flag=False, domains=set(), counter=0)
    domains = info[0]
    NSEC3_flag = info[1]
    pretty_print(domains, NSEC3_flag)


if __name__ == '__main__':
    main()
