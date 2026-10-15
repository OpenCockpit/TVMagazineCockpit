# User Guide

## The screen

```
+-----------------------------------------------------------------------------------+
| Data source - Bouquet: Favourites, Page: 1/4, Services: 22        < Wed, 21. Oct 2026 > |
+------------+------------+------------+------------+------------+-------------------+
| [picon]    | [picon]    | ...                                                      |  prime time
| [picture]  | [picture]  |                                                          |  (20:15)
| ARD        | ZDF        |                                                          |
| 20:15 Tatort | 20:15 ...|                                                          |
+------------+------------+------------+------------+------------+-------------------+
| 19:30 Tagesschau | 19:00 heute | ...                                                |
| 20:15 [NEU] Tatort | 19:25 ...                                                      |  programmes
|       Der Pott  (highlighted)                                                        |  (5 per column)
| 21:45 Tagesthemen | ...                                                              |
| 22:15 ...                                                                            |
+--------------------------------------------------------------------------------------+
| More ...       20:15         22:00         Now                       Menu    Info    |
+--------------------------------------------------------------------------------------+
```

- **Title bar:** the data source, the bouquet, the page number (`Page: 1/4`) and the number of channels (`Services`). While
  data is loading it says *Loading...*; if nothing is available for the page, *No event data available*.
- **Day selector** (top right): the chosen day, as `< Wednesday, 21. Oct 2026 >`.
- **Prime-time row:** one cell per column.
- **Programme lists:** one list per column, five rows tall.
- **Colour buttons:** *More ...*, *20:15*, *22:00*, *Now*, plus *Menu* and *Info* at the bottom.

## Columns, pages and channels

The channels of your bouquet are laid out **six per page**, in bouquet order. **LEFT** and **RIGHT** move between columns;
at the edge they turn the page and wrap around at the end. **CHANNEL+** and **CHANNEL-** turn a whole page. The
bouquet is the one set in [Settings](Settings.md#bouquet). Only channels that the plugin has an entry for, and that the chosen data
source can deliver, are shown (see [Channels](Channels.md)).

## The prime-time cell

At the top of each column:

| Part | Content |
|---|---|
| Picon | The channel's logo (Enigma2's standard picons) |
| Picture | A picture of the programme that runs at **20:15** on the chosen day |
| Channel name | In yellow |
| Time and title | Start time and title of the 20:15 programme |

It always shows the 20:15 programme (the one starting closest to that time), not the one you are looking at in the list. Changing the
day changes it. The picture appears a moment after the page, once it has been downloaded.

## The programme lists

Each column shows five programmes: the one before, the **selected** one, and three following. Each cell shows

| Part | Content |
|---|---|
| Start time | `HH:MM` |
| NEU | A badge under the time for a new episode (TV Spielfilm only) |
| Title | The programme title, wrapped |
| Grey line | The episode title / subtitle |
| Grey line | The production year (TV Spielfilm: country and year) |

The highlighted cell is the **selected** programme of the active column.

## All columns move together

The columns are **aligned on time**. When you press **DOWN** or **UP** in the active column, the selected
programme changes, and every other column scrolls to the programme that is running at the time of that one. So you
read the evening across all channels.

The three colour buttons jump all columns to a time on the chosen day:

| Button | Jumps to |
|---|---|
| **Green** | 20:15 |
| **Yellow** | 22:00 |
| **Blue** | The current time of day (*Now*) |

On first opening, the columns are at 20:15.

## Days

**NEXT** and **PREVIOUS** change the day. The range is **yesterday up to 14 days ahead**, 16 days in all. Going past either end
wraps around. After a change the columns are reloaded for the new day; data for days you have not looked at is
fetched as needed.

## Loading

When you open a page or a day for the first time, the programmes of its six channels are downloaded. The columns fill as
the data arrives; the title bar says *Loading...*. With TV Spielfilm, programme details (picture, NEU badge) are fetched in the
background for the programmes on screen, so the badges and the prime-time pictures appear a moment later.

Press **0** to reload the view.

## Detail and actions

- **OK** or **INFO** on a programme opens the [event details](Event-Details.md).
- **RED** (*More ...*) opens a menu to [zap, add a timer or search](Actions.md).
- **MENU** opens the [settings](Settings.md).
- **EXIT** closes the plugin.
