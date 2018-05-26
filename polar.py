#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""polar plot functions"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline
plotly.offline.init_notebook_mode(connected=False)


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


def _ipolarplot(df, layout=None, *args, **kwargs):
    """polar iplot
        usage:
            df.ipolarplot(layout=<layout>, mode=<mode>, marker=<marker>...)

        args:
            df: Data (pandas.Series or DataFrame object)
            layout: go.Layout args (dict like)
            *args, **kwargs: Scatterpolar args such as marker, mode...

        return:
            plotly.offline.iplot(data, layout)
    """
    if isinstance(df, pd.Series):  # Type Series
        data = [go.Scatterpolar(r=df, theta=df.index)]
    else:  # Type DataFrame
        data = list()
        for _data in df.columns:
            # Make polar plot data
            polar = go.Scatterpolar(
                r=df[_data], theta=df.index, name=_data, *args, **kwargs)
            data.append(polar)  # Append all columns in data
    # Use layout if designated
    fig = go.Figure(data=data) if not layout\
        else go.Figure(data=data, layout=go.Layout(layout))
    return plotly.offline.iplot(fig)


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
    setattr(cls, 'polarplot', _polarplot)
    setattr(cls, 'ipolarplot', _ipolarplot)
    setattr(cls, 'mirror', _mirror)
