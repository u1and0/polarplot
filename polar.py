#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""polar plot functions"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def _polarplot(df, **kwargs):
    """polar plot
    usage: df.polarplot()
    Same args with `df.plot()`
    """
    _df = df.copy()
    _df.index = _df.index * np.pi / 180  # Convert radian
    ax = plt.subplot(111, projection='polar')  # Polar plot
    ax = _df.plot(ax=ax, **kwargs)
    return ax


def _mirror(df, ccw=True):
    """Make a mirror copy of DataFrame with respect to the line
    usage:
        df.mirror(ccw=True)...data increase to Counter Clock Wise(ccw)
        df.mirror(ccw=False)...data increase to Clock Wise(cw)
    args: ccw(bool) default True
    return: pandas.Series or pandas.DataFrame
    """
    copy_index = df.index
    if ccw:  # data increase to Counter Clock Wise(ccw)
        mirror_df = df.append(df.iloc[-2::-1], ignore_index=True)
        new_index = np.r_[copy_index, copy_index[1:] + copy_index[-1]]
    else:  # data increase to Clock Wise(cw)
        mirror_df = df.iloc[::-1].append(df.iloc[1:], ignore_index=True)
        new_index = np.r_[copy_index[::-1], -copy_index[1:]]
    mirror_df.index = new_index  # reset index
    return mirror_df


# Use as pandas methods
for cls in (pd.DataFrame, pd.Series):
    setattr(cls, 'mirror', _mirror)
    setattr(cls, 'polarplot', _polarplot)
