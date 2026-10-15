# Architecture

For developers.

## Overview

```
 plugin menu / extensions menu                 autostart (once per Enigma2 start)
        |                                            |
  TVMagazineCockpit (Screen + More + Picture)    Cache: cleanup(), downloadEvents(), downloadPictures()
        |
        +-- Navigation   (column, page, day, time)
        +-- Page         (draws a page of six columns, triggers downloads)
        +-- Column       (draws one column, resolves details, prime-time cell)
        +-- TVMagazineData -> TVFAData | TVMData | TVSData     (threads; JSON or HTML)
        +-- EventDetails (details screen, trailer through CockpitPlayer)
        +-- More         (zap, timer, Mediathek, TMDB)
```

## Source files

| File | Role |
|---|---|
| `plugin.py` | Descriptors: autostart (builds the daily cache), plugin and extensions menu entry, skin change |
| `TVMagazineCockpit.py` | The main screen: widgets (`list0..5`, `channel0..5`, `picon0..5`, `programpix0..5`, `time0..5`, `description0..5`, `day_selector`, the buttons), the action map, settings callback, reload |
| `Navigation.py` | State: `list_index` (column), `page_index`, `pages`, the chosen day (`_selected_day`, 0 = yesterday ... 15), and the helpers `getTimestamp("HH:MM")`, `moveUp/Down`, `left/right`, `channelup/down`, `key_next/back` |
| `Page.py` | `showPage`: slices six channels, shows each column, starts the download for channels without data, sets the title |
| `Column.py` | `showColumn`, `updateEventList`, `showPrimeEvent`; asynchronous detail resolution with a coalesced refresh |
| `TVMagazineData.py` | Chooses the data-source class; `getDetailedEvent` (only TVS has details) and `getDetailedEventAsync` |
| `TVFAData.py`, `TVMData.py`, `TVSData.py` | The three sources: `downloadEvents(day, channels, all_events, callback)` runs in a thread |
| `TVSUtils.py` | HTML parsing for TV Spielfilm: `tvs_parse` (list page) and `tvs_parse_details` (programme page) |
| `Cache.py`, `CacheUtils.py` | The daily cache: `events.json` read / write, start-up download and cleanup |
| `ChannelUtils.py` | Channel dictionary, bouquet handling, `readChannelList`, `getCurrentBouquetName` |
| `EventUtils.py` | `find_time_event_index`: the programme whose start is closest to a time |
| `DateTimeUtils.py` | ISO time parsing, midnight of a day, `get_day_details` |
| `EventDetails.py` | The details screen |
| `More.py` | The actions menu; timer creation and conflict handling |
| `ZapUtils.py` | `zapService`: select the service in its bouquet and zap |
| `Picture.py` | Download and decode pictures (`ePicLoad`), with a per-path cache |
| `EventList.py` | The `List` source for a column (selection enable, move, hide / show) |
| `CockpitPlayer.py` | Trailer player: `MoviePlayer` without info bar |
| `Index.py` | The index map of the event record |
| `ConfigInit.py` | `COLS = 6`, `ROWS = 5`, settings, `data_sources` |
| `setup.xml`, `SetupScreen.py`, `keymap.xml` | Settings and keys (`TVC_Actions`) |
| `tvc_channel_dict.json` | The channel dictionary |
| `channels/master_channels.json`, `test/` | Source data and scripts for generating the dictionary |

Shared helper modules (`WebRequests`, `ServiceUtils`, `FileUtils`, `ChannelListUtils`, `PluginUtils`, `SkinUtils`, `Debug`) come from the `Common`
repository.

## The event record

A programme is a **list** (JSON arrays in the cache) of `len(idx) + 1` values. `Index.py` names the positions:

| Index | Name | Content |
|---|---|---|
| 0 | `startHM` | `HH:MM` |
| 1 | `title` | Title |
| 2 | `subtitle` | Subtitle / episode title |
| 3 | `year` | Production year (TVS: country and year) |
| 4 | `startTime` | Epoch seconds |
| 5 | `country` | Country |
| 6 | `category` | Category |
| 7 | `genre` | Genre |
| 8 | `endTime` | Epoch seconds |
| 9 | `is_new` | `None` = details not fetched yet, `False`/`True` afterwards |
| 10 | `duration` | Minutes |
| 11 | `channel` | Channel name from the source |
| 12 | `urlsendung` | URL of the programme's page (TVS and TVM); empty for TVFA |
| 13 | `has_video` | A video is announced |
| 14 | `photo_url` | Picture address |
| 15 | `description` | Long description |
| 16 | `video_url` | Trailer address |

The skin addresses the first fields by number (`value: 0` start time, `1` title, `2` subtitle, `3` year, `9` the NEU badge), so the order is
part of the skin interface. The display list pads short entries to the length of `is_new` + 1: an entry that is too short once crashed
`eListboxPythonMultiContent` in its C++ painting code.

## Data flow

1. `Page.showPage` takes the six channels of the current page (`channel_list[page * 6 : page * 6 + 6]`) and, for each, looks in
   `events[date][service_ref]`. Channels without data are collected.
2. If any are missing and this is the first pass, `TVMagazineData.downloadEvents` starts a worker thread
   (`threads.deferToThread`). It merges the results into `events`, saves `events.json`, and calls back on the reactor thread with the merged
   dictionary, which re-enters `showPage(events)`. The second pass never starts another download, so a channel with no data settles on "no data".
3. `Column.showColumn` finds the event closest to the chosen timestamp, shows the five events from one before it, and starts asynchronous
   detail fetches for the visible events that have none (`resolveEventDetails`). Results come back with `reactor.callFromThread`.
4. Resolved columns are not redrawn one by one. They are collected and redrawn together by a 150 ms timer, because many `setList()` calls in a
   short time crashed Enigma2.
5. The prime-time cell shows the event closest to 20:15 of the chosen day, and its picture once `photo_url` is known.
6. `Navigation.moveUp/Down` set the shared `timestamp` to the selected event's start; the next `showPage` aligns all columns to it.

When the screen closes, `Column.cancelPendingRefresh` drops its reference to the screen so late callbacks do nothing.

## Threads

Network access happens only in worker threads (`deferToThread`), never in the screen. The exception is `key_ok`, which calls
`getDetailedEvent` synchronously for the selected programme (a single page fetch for TVS).

## The skin

Source files are YAML parts compiled to `skin/default/skin.xml`:

| Part | Content |
|---|---|
| `screen_TVMagazineCockpit.ymlinc` | The 1920 x 1080 main screen: title bar, `day_selector`, six prime-time cells, six `Listbox` widgets of 320 x 750 at y = 275, footer. A `.zmlinc` variant of the same screen generates the six repeats with a `for` loop |
| `screenpart_PrimeCell.ymlinc` | One prime-time cell: picon, picture, channel, time, title |
| `screenpart_EventCell.ymlinc` | The `TemplatedMultiContent` for one list cell (150 high): start time, NEU badge, title, subtitle, year |
| `screen_EventDetails.ymlinc` | The details screen, 1800 x 930 |

Font names in a cell's `fields` must also appear in the cell's `fonts:` list, otherwise `yml2xml` stops with a `KeyError`.

## Packaging and translations

Autotools. `CONTROL/control` lists the dependencies; `po/de.po` and `po/setup.po` carry the German texts. `src/Makefile.am` installs the `*.json` files
next to the code, and `channels/Makefile.am` installs the master list.
