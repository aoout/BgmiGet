# BgmiGet

## How to Install

```
pip install git+https://github.com/aoout/BgmiGet.git@dev 
```

## Basic Usage

Search anime by search "commnad".

```
bgmiget search '因为太怕痛' 7 "sc" "桜都字幕组"
>0  -> 【因为太怕痛...】【07】【桜都字幕组】
```

Then, download anime by index.

```
bgmiget download 0
```

## 更多功能

说实话，其实我也不知道应该再添加什么功能好了。不是因为有一些事情能力不足以做到，而是说没有办法发现新的需求了。订阅，更新啊，这些实际上我并不需求。用那样的数据源没办法做好。比如说，我追番的时候，看的字幕组可能会换。那么订阅的话就很难做。

自动上传阿里云盘这种想法也有过，不过果然那种不稳定的东西还是算了。api什么的也有可能会被换掉吧。扫码登陆也不太优雅。、

目前还没有合并分支，单纯只是想自己先用一用，修一修bug，加一些解析的规则。