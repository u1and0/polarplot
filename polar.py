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
    _df.index = _df.index * np.pi / 180  # ラジアン変換
    ax = plt.subplot(111, projection='polar')  # 極座標プロット
    ax = _df.plot(ax=ax, kind='line', **kwargs)
    return ax


def _mirror(self, axis=0):
    """Make a mirror copy of DataFrame with respect to the line

    usage:
        df.mirror(0) ...same as df.mirror() or df.mirror('x')
        df.mirror(1) ...same as df.mirror('y')

    args: axis: (0|1|x|y)
    return: pandas.Series or pandas.DataFrame
        """
    index = self.index  # copy of index
    df = self.append(self.iloc[-2::-1], ignore_index=True)  # mirror data
    new_index = {
        0: np.r_[index, -index[-2::-1]],  # 0 or xのとき、水平線に対する鏡像
        1: np.r_[index, index[1:] + index[-1]],  # 1 or yのとき、垂直線に対する鏡像
        'x': np.r_[index, -index[-2::-1]],
        'y': np.r_[index, index[1:] + index[-1]],
    }
    df.index = new_index[axis]  # reset index
    return df


# 関数のメソッド化
for cls in (pd.DataFrame, pd.Series):
    setattr(cls, 'mirror', _mirror)
    setattr(cls, 'polarplot', _polarplot)
