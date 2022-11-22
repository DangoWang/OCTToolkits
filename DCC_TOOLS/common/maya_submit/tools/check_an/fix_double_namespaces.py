#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/5/23

import os
import codecs
import re
import shutil


def get_maya_references(file_path, pattern='rfn[\S\s]*-typ'):
    data = list()
    # str_format = re.compile(pattern)
    with codecs.open(file_path, 'r', 'gbk') as ma:
        for line in ma.readlines():
            if line.count('requires'):
                break
            if ':' in line and 'RN' in line:
            # if str_format.search(line):
                data.append(line.split('-rfn')[1].split("\"")[1])
    return data


def get_double_namespaces(ref_data):
    double_names = [data for data in ref_data if ":" in data]
    double_names_dict = {}
    for each in double_names:
        double_names_dict[each] = each.split(':')[-1]
    return double_names_dict


def fix_double_namespaces(file_path):
    ref_data = get_maya_references(file_path)
    if not ref_data:
        return
    double_data = get_double_namespaces(ref_data)
    print double_data
    if os.path.isfile(file_path):
        with codecs.open(file_path, 'r', encoding='gbk') as (f):
            file_content = f.read()
        file_context = file_content
        for k, v in double_data.iteritems():
            file_context = file_context.replace(k, v)
        old_file_path = file_path.replace('.ma', '_dirty.ma')
        shutil.copy2(file_path, old_file_path)
        with codecs.open(file_path, 'w', encoding='gbk') as nf:
            nf.write(file_context)
    return True


if __name__ == '__main__':
    str_ = raw_input("input file:")
    fix_double_namespaces(str_)

