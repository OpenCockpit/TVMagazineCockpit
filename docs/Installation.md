# Installation

## Requirements

- An Enigma2 box with a Python 3 based image (OpenViX and compatible).
- An **Internet connection**. The programme data and pictures come from websites.
- A directory `/data` that is writable (the cache lives in `/data/TVC`).
- Channels in a bouquet that the plugin knows (see [Channels](Channels.md)).

## Package

`enigma2-plugin-extensions-tvmagazinecockpit`, architecture independent. It depends on:

| Package | Why |
|---|---|
| `enigma2-plugin-skincomponents-componentscockpit` | Skin components |
| `enigma2-plugin-systemplugins-covercockpit` | Cockpit family dependency |
| `enigma2-plugin-systemskins-fontcockpit` | Fonts |

Install it and **restart Enigma2**.

## Where it appears

The plugin menu and the extensions menu (blue button): **TVMagazineCockpit**, described as "Browse TV Magazine".

## What happens at start-up

When Enigma2 starts, the plugin prepares today's data in the background so that the first open is quick:

1. Folders of earlier days in `/data/TVC` are deleted.
2. If there is no cache file for today yet, the programmes of **all channels of your bouquet** are downloaded for today.
3. Then, in a background thread, the pictures of the 20:15 programmes are downloaded.

This happens once per day. Opening the plugin later the same day reads the cache. Details are on the [Cache](Cache.md) page.

On a box that is started only to record, with no Internet access, the download simply fails and is tried again the
first time you open the plugin.

## Removing

Remove the package with the package manager. The cache folder `/data/TVC` can be deleted by hand. Your own channel
dictionary in `/etc/enigma2/tvc_channel_dict.json`, if you made one, stays.
