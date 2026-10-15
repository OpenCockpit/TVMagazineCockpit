# Actions

Press **RED** (*More ...*) on a programme to open a menu of things to do with it. The menu works on the **selected** programme
of the active column.

| Entry | Shown | Does |
|---|---|---|
| **Zap** | always | Switches to the channel and closes the plugin |
| **Add Timer** | always | Opens Enigma2's timer editor for the programme |
| **Mediathek search** (the plugin's description) | if MediathekCockpit is installed | Opens MediathekCockpit with the programme's title searched |
| **TMDB search** (the plugin's description) | if TMDBCockpit is installed | Opens TMDBCockpit's information for the title |

If the active column has no programme (no data), the menu does not open.

## Zap

The channel is selected in your channel list in the bouquet that contains it (the right bouquet is entered first), and
then zapped to. The plugin closes, so you see the programme. If the channel is not in any bouquet, the
list for all services is used.

## Add Timer

The timer editor opens, filled in with

| Field | Value |
|---|---|
| Channel | The channel of the column |
| Begin | The programme's start time **minus your "margin before"** (Enigma2 setting, in minutes) |
| End | The programme's end time **plus your "margin after"** |
| Name and description | The title and the subtitle |
| Directory | Your preferred timer directory |

Press the timer editor's **save** to create the timer. If the new timer overlaps with an existing one, the plugin first tries to
resolve it by extending the earlier timer's end ("auto increase") and records again. If a conflict remains, Enigma2's
timer conflict dialog opens for you to decide.

Timers made from the TV magazine are normal timers: they appear in the timer list and, when they record, in MovieCockpit like any
other recording. With MovieCockpit installed the recording gets the programme's data from the broadcast, not from the magazine.

## Mediathek search

If the programme is available in a Mediathek, MediathekCockpit finds it from the title. Choosing the entry opens the plugin with the title in the
search box. See the MediathekCockpit wiki ([Integration](../../MediathekCockpit/docs/Integration.md)).

## TMDB search

Opens TMDBCockpit's movie information for the title. See the TMDBCockpit documentation.
