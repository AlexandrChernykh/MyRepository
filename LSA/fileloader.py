from os import listdir

__subdirs = listdir("./DATA/")

__files = []
for i in range(0, len(__subdirs)):
    __files.append([["./DATA/"+__subdirs[i]+"/"+x, x] for x in listdir("./DATA/"+__subdirs[i]+"/")])


def get_groups_amount():
    return len(__subdirs)


def get_group_names():
    return __subdirs


def get_group(id, return_name):
    if return_name:
        return __files[id], __subdirs[id]
    else:
        return __files[id]

