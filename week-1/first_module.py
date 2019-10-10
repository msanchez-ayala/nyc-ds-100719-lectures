# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def calc_mean(data):
    return sum(data)/len(data)

def calc_median(data):
    data.sort()
    n = len(data)
    if n % 2:
        return data[n//2]
    else:
        return (data[(n//2)-1] + data[n//2])/2
