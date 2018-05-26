
![Peek 2018-05-27 01-10.gif](https://qiita-image-store.s3.amazonaws.com/0/113494/9fe51d31-caca-c6dd-9374-54f6e739c1e5.gif)

![polarplot_33_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/489dcdd9-76fc-fb9b-0d83-7bbed18029a9.png)


最終的にデータフレームからこんな極座標プロットを描けるようにします。
matplotlibを利用してのプロットはコードが煩雑になりやすいので、なるべくpandas.DataFrameのメソッドとして呼び出してコンパクトなコードでプロットできるようにします。

# モジュールインポート


```python
import polar
```

使用するコードはこれだけです。

```python:polar.py
#!/usr/bin/env python
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
```

# Seriesで極座標プロット

## サンプルデータ
10°刻みで0°から90°までランダムな値が入ったデータを用意します。
以下では断りがない限り、indexの単位はすべて度数法に準じた"°(度)"です。


```python
np.random.seed(6)  # ランダムステート固定
index = range(0,190,10)
sr = pd.Series(np.random.randn(len(index)), index=index); sr
```




    0     -0.311784
    10     0.729004
    20     0.217821
    30    -0.899092
    40    -2.486781
    50     0.913252
    60     1.127064
    70    -1.514093
    80     1.639291
    90    -0.429894
    100    2.631281
    110    0.601822
    120   -0.335882
    130    1.237738
    140    0.111128
    150    0.129151
    160    0.076128
    170   -0.155128
    180    0.634225
    dtype: float64



## 極座標プロット
`polarplot()`メソッドでサンプルデータを極座標にプロットします。
`polar.py`をインポートしてしまえば、`pandas.Series`, `pandas.DataFrame`型から`polarplot()`メソッドが使えるようになっています。


```python
sr.polarplot()
```

![polarplot_8_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/806ec950-11d9-e8d2-e13a-6a064bd4ee4a.png)



```python:polarplot.py
def _polarplot(df, **kwargs):
    _df = df.copy()
    _df.index = _df.index * np.pi / 180  # Convert radian
    ax = plt.subplot(111, projection='polar')  # Polar plot
    ax = _df.plot(ax=ax, **kwargs)
    return ax
```

`polarplot()`メソッドは引数にデータフレーム(またはシリーズ)を要求して、戻り値はグラフaxです。
`**kwargs`引数で、`df.plot()`と同じ引数が使えます。

pandasのメソッドとして使えるように、ファイルの一番下で`setattr(pd.DataFrame, 'polarplot', _polarplot)`としてあるので、`df.polarplot()`として呼び出せます。

`pd.DataFrame.polarplot = _polarplot`とすることと同じです。自作の関数を既存クラスのメソッドとして扱えるようにする私の常套手段です。

## 鏡像データを作成
`mirror()`メソッドで、鏡像データを作り出します。

データの中身は次に示すように360°方向に増えます。


```python
sr.mirror()
```




    0     -0.311784
    10     0.729004
    20     0.217821
    30    -0.899092
    40    -2.486781
    50     0.913252
    60     1.127064
    70    -1.514093
    80     1.639291
    90    -0.429894
    100    2.631281
    110    0.601822
    120   -0.335882
    130    1.237738
    140    0.111128
    150    0.129151
    160    0.076128
    170   -0.155128
    180    0.634225
    190   -0.155128
    200    0.076128
    210    0.129151
    220    0.111128
    230    1.237738
    240   -0.335882
    250    0.601822
    260    2.631281
    270   -0.429894
    280    1.639291
    290   -1.514093
    300    1.127064
    310    0.913252
    320   -2.486781
    330   -0.899092
    340    0.217821
    350    0.729004
    360   -0.311784
    dtype: float64



```python:mirror.py
def _mirror(df, ccw=True):
    copy_index = df.index
    if ccw:  # data increase to Counter Clock Wise(ccw)
        mirror_df = df.append(df.iloc[-2::-1], ignore_index=True)
        new_index = np.r_[copy_index, copy_index[1:] + copy_index[-1]]
    else:  # data increase to Clock Wise(cw)
        mirror_df = df.iloc[::-1].append(df.iloc[1:], ignore_index=True)
        new_index = np.r_[copy_index[::-1], -copy_index[1:]]
    mirror_df.index = new_index  # reset index
    return mirror_df
```

引数無し、または`ccw=True`で`mirror()`メソッドを呼ぶと、反時計回りにデータをコピーして、インデックスを振り直します。
引数`ccw=False`で`mirror()`メソッドを呼ぶと、時計回りにデータをコピーして、インデックスを振り直します。

mirror化したシリーズをプロットします。


```python
sr.mirror().polarplot()
```


![polarplot_16_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/70e9ea75-ae07-0c67-c2e7-44e3c10805bf.png)



# DataFrameで極座標プロット

## sin波サンプルデータ
次に、DataFrame型で極座標プロットを行います。
sin波を$\pi$/2だけとったサンプルデータを作成します。

SeriesだろうがDataFrameだろうが使い方は同じです。


```python
index = np.arange(0,100,10)
df = pd.DataFrame({'sin wave':np.sin(index*np.pi/180),
                   '3sin wave':np.sin(3*index*np.pi/180)}, index=index)
df.plot(style='o-')
```



![polarplot_19_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/78ffb037-8270-225e-57f9-c475164979d7.png)



## polarplotの引数指定

極座標プロットするために`polarplot()`メソッドを使用します。
`polarplot()`メソッドの引数には`df.plot(**kwargs)`として使えるほぼすべての引数が使えます。

例えば以下のようにして`style`や`ms`を指定してあげると、線種を変えたり、marker sizeを変更してくれます。


```python
df.polarplot(style='d--', ms=5,
             ylim=[0,1.2], yticks=np.arange(0,1.2,.2),
             xticks=np.arange(1,360,15)*np.pi/180)
```


![polarplot_24_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/d8feb7c5-2eec-6459-0123-e83ca7067fa6.png)




## ミラー化(CCW=反時計回り)
デフォルトでは、`mirror()`メソッドは反時計回りに鏡像を作成します。


```python
df.mirror()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sin wave</th>
      <th>3sin wave</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>40</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>50</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>60</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>70</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>80</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>90</th>
      <td>1.000000</td>
      <td>-1.000000e+00</td>
    </tr>
    <tr>
      <th>100</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>110</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>120</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>130</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>140</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>150</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>160</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>170</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>180</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>



デカルト座標系にプロットするとこんな感じです。


```python
df.mirror().plot()
```

![polarplot_26_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/841fdf18-9e87-0a56-d00f-532ef2c207eb.png)



極座標プロットでは判例が間違いなくグラフの円の中に含まれて重なって見づらいので、凡例を外側に置くように`plt.legend()`で凡例の位置を指定したほうが良いです。


```python
df.mirror().polarplot()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)  # 凡例外側
```



![polarplot_28_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/0d8be73c-7a78-d771-e723-67cd5fa641e9.png)



1周(360度)までデータを拡張するには`mirror()`メソッドを2回続けて打って下さい。


```python
df.mirror().mirror()
```




<div>
<style scoped>

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sin wave</th>
      <th>3sin wave</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>40</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>50</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>60</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>70</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>80</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>90</th>
      <td>1.000000</td>
      <td>-1.000000e+00</td>
    </tr>
    <tr>
      <th>100</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>110</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>120</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>130</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>140</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>150</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>160</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>170</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>180</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>190</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>200</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>210</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>220</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>230</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>240</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>250</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>260</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>270</th>
      <td>1.000000</td>
      <td>-1.000000e+00</td>
    </tr>
    <tr>
      <th>280</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>290</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>300</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>310</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>320</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>330</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>340</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>350</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>360</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.mirror().mirror().plot()
```


![polarplot_31_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/ee1ed87e-880b-53b2-c0f9-87bc5d2e3f89.png)




```python
df.mirror().mirror().polarplot(df.polarplot(style='d--', ms=5,
                               ylim=[0,1.2], yticks=np.arange(0,1.2,.2),
                               xticks=np.arange(1,360,15)*np.pi/180))
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)  # 凡例外側
```


![polarplot_33_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/489dcdd9-76fc-fb9b-0d83-7bbed18029a9.png)



## ミラー化(CW=時計回り)
`mirror()`メソッドの引数は`cw`(Counter Cloce Wise 反時計回り)のみで、デフォルトは`True`です。
`mirror(False)`のようにしてメソッドの引数を指定すると`cw`(Cloce Wise 時計回り)でデータを作成します。


```python
df.mirror(False)
```




<div>
<style scoped>

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sin wave</th>
      <th>3sin wave</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>90</th>
      <td>1.000000</td>
      <td>-1.000000e+00</td>
    </tr>
    <tr>
      <th>80</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>70</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>60</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>50</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>40</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>30</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>20</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>0</th>
      <td>0.000000</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>-10</th>
      <td>0.173648</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>-20</th>
      <td>0.342020</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>-30</th>
      <td>0.500000</td>
      <td>1.000000e+00</td>
    </tr>
    <tr>
      <th>-40</th>
      <td>0.642788</td>
      <td>8.660254e-01</td>
    </tr>
    <tr>
      <th>-50</th>
      <td>0.766044</td>
      <td>5.000000e-01</td>
    </tr>
    <tr>
      <th>-60</th>
      <td>0.866025</td>
      <td>1.224647e-16</td>
    </tr>
    <tr>
      <th>-70</th>
      <td>0.939693</td>
      <td>-5.000000e-01</td>
    </tr>
    <tr>
      <th>-80</th>
      <td>0.984808</td>
      <td>-8.660254e-01</td>
    </tr>
    <tr>
      <th>-90</th>
      <td>1.000000</td>
      <td>-1.000000e+00</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.mirror(False).plot()
```



![polarplot_35_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/18c13e6d-3c77-8a48-c587-4434207ce307.png)




```python
df.mirror(False).polarplot()
```


![polarplot_36_1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/64960e1a-f17f-4f7c-494e-65add3e2bdba.png)



# 動的プロット
 [Polar Charts in Python](https://plot.ly/python/polar-chart/)を参考にplotlyを利用してインタラクティブな極座標プロットを描いてみます。

まずはplotlyのインポートとオフラインモードの有効化


```python
import plotly.graph_objs as go
import plotly.offline
plotly.offline.init_notebook_mode(connected=False)
```

データをリスト型にして`go.Figure()`クラスの引数とします。

```python
data = [
    go.Scatterpolar(
        r = df['sin wave'],
        theta = df.index,
    ),
    go.Scatterpolar(
        r = df['3sin wave'],
        theta = df.index,
    )
]

fig = go.Figure(data=data)
plotly.offline.iplot(fig)
```

![newplot.png](https://qiita-image-store.s3.amazonaws.com/0/113494/70b021a5-cbdc-df16-feff-1ea4af046a2b.png)

これを参考に`polarplot()`をまねて`ipolarplot()`を作成しました。

```python:_ipolarplot.py
def _ipolarplot(df, layout=None, *args, **kwargs):
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

for cls in (pd.DataFrame, pd.Series):
    setattr(cls, 'ipolarplot', _ipolarplot)
```

```python
sr.ipolarplot()
```

![newplot1.png](https://qiita-image-store.s3.amazonaws.com/0/113494/18999974-0a8e-86b7-6614-86644eab50bd.png)



```python
df.ipolarplot()
```

![Peek 2018-05-27 01-10.gif](https://qiita-image-store.s3.amazonaws.com/0/113494/9fe51d31-caca-c6dd-9374-54f6e739c1e5.gif)


`**kwargs`として、`go.Scatter()`に渡す引数と同じものが使えます。
レイアウトは辞書型として内部的に`go.Layout()`に渡しています。


```python
df.mirror().ipolarplot(mode='markers', layout=dict(title='sin & 3sin', showlegend=False))
```

![newplot3.png](https://qiita-image-store.s3.amazonaws.com/0/113494/c7fa5e4f-7715-cddf-f87f-5906db3ffe45.png)



塗りつぶしやレンジ、ティックスの幅を変えることもできますが、plotlyの指定の仕方はやや複雑です。

plotly polarchartの複雑な設定は先にも挙げた[Polar Charts in Python](https://plot.ly/python/polar-chart/)を参考にしました。


```python
df.mirror().mirror().ipolarplot(fill='toself',
                                layout=dict(
                                    polar=dict(
                                        radialaxis = dict(
                                                        visible=True,
                                                        range=[0,1.2],
                                                    ),
                                        angularaxis = dict(
                                                        dtick=15
                                                        )
                                            )
                                       )
                                )
```


![newplot4.png](https://qiita-image-store.s3.amazonaws.com/0/113494/e3d4d62e-42ac-2081-da99-85623a6e3743.png)




# まとめ
polar.pyを使用して次のことができました。

* `polarplot()`メソッドによりデータフレームから極座標プロットをメソッドとして扱えるようになりました。
* `mirror()`メソッドにより線対称にデータを増やすことが可能になりました。
* plotlyを利用した`ipolarplot()`メソッドを使用して、ズームイン、ズームアウト、数値をインタラクティブに表示可能なプロットを描けました。

コードとjupyter notebookはgithubにあげました。
[u1and0/polarplot](https://github.com/u1and0/polarplot)













