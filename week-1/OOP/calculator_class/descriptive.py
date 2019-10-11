# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class Calculator:
    
    def __init__(self,data):
        self.data = data
        self.__calc_all(self.data)
        
    def __calc_all(self,data):
        self.length = len(self.data)
        self.mean = self.__calc_mean(data)
        self.median = self.__calc_median(data)
        self.variance = self.__calc_variance(data)
        self.stand_dev = self.variance**0.5
    
    def __calc_mean(self, data):
        return sum(data)/len(data)
    
    def __calc_median(self, data):
        data = sorted(data)
        n = len(data)
        if n % 2:
            return data[n//2]
        else:
            return (data[n//2] + data[(n-1)//2]) / 2
    
    def __calc_variance(self, data):
        numerator = []
        for num in data:
            numerator.append((num - self.mean)**2)
        return sum(numerator)/(len(numerator)-1)
        
    def add_data(self,new_data):
        self.data = self.data + new_data
        self.__calc_all(self.data)
    
    def remove_data(self, del_data):
        for num in del_data:
            if num in self.data:
                while num in self.data: 
                    self.data.remove(num)
        self.__calc_all(self.data)
        
    
    