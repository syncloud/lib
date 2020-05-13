from os import makedirs, chown, utime
from os.path import isdir
from grp import getgrnam
from pwd import getpwnam
from shutil import rmtree
from subprocess import check_output


def makepath(path):
    if not isdir(path):
        makedirs(path)


def removepath(path):
    if isdir(path):
        rmtree(path, ignore_errors=True)


def createfile(filepath):
    try:
        f = open(filepath, 'w+')
        f.close()
    except:
        pass


def chownpath(path, user, recursive=False):
    if recursive:
        chownrecursive(path, user)
    else:
        chown(path, getpwnam(user).pw_uid, getgrnam(user).gr_gid)


def chownrecursive(path, user):
    estimate_count = int(check_output('find {0} -maxdepth 3 | wc -l'.format(path), shell=True).decode())
    if estimate_count > 1000:
        return 'not changing permissions, too many files'

    return check_output('chown -RLf {0}. {1}'.format(user, path), shell=True).decode()


def touchfile(file):
    with open(file, 'a'):
        utime(file, None)