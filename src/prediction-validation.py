#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 08:52:39 2018

@author: Wanlu
"""

import pandas as pd
import numpy as np
import sys

(window_path, actual_path, pred_path, output_path) = sys.argv[1:]
# ./input/window.txt ./input/actual.txt ./input/predicted.txt ./output/comparison.txt

actual = pd.read_csv(actual_path, sep = '|', header = None)
actual.columns = ['time', 'stock', 'price']

predicted = pd.read_csv(pred_path, sep = '|', header = None)
predicted.columns = ['time', 'stock', 'price']

time_window = int(open(window_path, 'r').readline())

error = pd.merge(actual, predicted, on = ['time', 'stock'], how = 'outer')
error['error'] = abs(error['price_x'] - error['price_y'])

time_grouped = error.groupby('time')
time_grouped = time_grouped['error'].aggregate([np.mean, 'count']).rename(columns = {'count': 'weight'})
time_grouped = time_grouped.reset_index()

def create_comparison(k):
    time1 = []
    time2 = []
    average_error = []
    for i in range(min(time_grouped['time']), max(time_grouped['time'])-k+2):
        time1.append(i)
        time2.append(i+k-1)
        if time_grouped['weight'].iloc[i-1:i+k-1].sum() != 0:
            average_error.append('{0:.2f}'.format(float((time_grouped['mean']*time_grouped['weight']).iloc[i-1:i+k-1].sum()/time_grouped['weight'].iloc[i-1:i+k-1].sum())))
        else:
            average_error.append(np.nan)
    time1 = pd.Series(time1)
    time2 = pd.Series(time2)
    average_error = pd.Series(average_error)
    table = pd.DataFrame({'time1':time1, 'time2':time2, 'average_error':average_error})
    return table[["time1", "time2", "average_error"]]

comparison = create_comparison(time_window)

# f = open(output_path, 'w')
comparison.to_csv(output_path, index = False, sep = '|', header = None)
# f.close()
