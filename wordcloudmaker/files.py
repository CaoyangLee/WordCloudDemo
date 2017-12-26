# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil


# 获取当前的目录
def get_dir():
    return str(os.path.abspath('.'))


# 创建新目录 判断是否已经存在
def create_dir(file, directory=get_dir()):
    path = os.path.join(directory, file)
    if not os.path.exists(path):
        os.mkdir(path)
        print('createDirs success')
    else:
        print('dirs is exist')
    return str(path)


# 删除空目录
def delete_dir(file, directory=get_dir()):
    path = os.path.join(directory, file)
    if os.path.exists(path):
        os.rmdir(path)


# 删除目录  强力删除
def delete_dir_with_child(file, directory=get_dir()):
    path = os.path.join(directory, file)
    if os.path.exists(path):
        try:
            os.rmdir(path)
        except OSError as e:
            shutil.rmtree(path)
        finally:
            print('deleteDir success')


# 创建一个文本
def create_file(file, directory=get_dir()):
    path = os.path.join(directory, file)
    if not os.path.exists(path):
        with open(directory + '/' + file, 'wb') as f:
            pass
    else:
        print('file is exist')
    return str(path)


# 删除文件
def delete_file(file, directory=get_dir()):
    path = os.path.join(directory, file)
    print(str(path))
    if os.path.exists(path):
        os.remove(path)
        print('deleteFile success')
    else:
        print('not exitst')


# 重新命名
def re_file_name(old_name, new_name, old_file_dir=get_dir(), new_file_dir=get_dir()):
    old_file = os.path.join(old_file_dir, old_name)
    if not os.path.exists(old_file):
        raise FileNotFoundError('file not exitst')
        pass
    new_file = os.path.join(new_file_dir, new_name)
    os.rename(old_file, new_file)
    print('rename success')


# 获取当前目录的所有文件或文件夹
def get_list_dir(directory=get_dir()):
    return [x for x in os.listdir(directory)]

