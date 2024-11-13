# 📺 BgmiGet

## 🌟 Overview

BgmiGet is a command line tool that allows you to search, download, and manage your favorite anime. It provides a simple and efficient way to keep track of the latest episodes and download them with ease.

## 📦 Dependencies

> [!NOTE]
> PyPdf requires Python 3.8.1.

## 💻 Installation

To install BgmiGet, you can use pip:
```
pip install bgmiget
```

## 🎬 Basic Usage

### 🔍 Searching Anime

To search for anime, use the "search" command. The format is as follows:
```
bgmiget search <anime_name> <episode_number> "<source>" "<subtitle_group>"
```
For example:
```
bgmiget search "因为太怕痛" 7 "sc" "桜都字幕组"
```
This will search for the anime "因为太怕痛" with episode number 7 from source "sc" and subtitle group "桜都字幕组". The result will be displayed as:
```
>0  -> 【因为太怕痛...】【07】【桜都字幕组】
```

### 🚀 Downloading Anime

Once you have found the anime you want, you can download it by its index. For example, to download the anime with index 0:
```
bgmiget download 0
```

### 🔄 Subscribing and Listing Anime

To subscribe to an anime, use the "subscribe" command. To list all subscribed anime, use the "show_subscribed" command.

### ⬆️ Upgrading Anime

To check for updates on subscribed anime, use the "upgrade" command. This will ensure you always have the latest episodes of your subscribed anime.
