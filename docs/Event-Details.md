# Event Details

Press **OK** or **INFO** on a programme to open its details.

```
+----------------------------------------------------------------+
| [picon]  Title (year)                         |  [picture]      |
|          Subtitle                             |                 |
|          20:15, 90 min                        |                 |
|  Description ...                              |                 |
|  ...                                          |                 |
|                                               |                 |
| Back                         Trailer                              |
+----------------------------------------------------------------+
```

| Field | Content |
|---|---|
| Picon | The channel's logo |
| Title | The programme title, with the production year in brackets if known |
| Subtitle | The episode title or subtitle |
| Time | Start time and duration in minutes (TV Für Alle and TV Spielfilm deliver a fractional value, so you may see `90.0 min`) |
| Description | The long description. Scrolls with the arrow keys when it is longer than the screen |
| Picture | A picture of the programme, shown if the source has one. It is downloaded on first use and kept in the [cache](Cache.md) |

## What you see depends on the source

Not every [data source](Data-Sources.md) delivers everything:

| | TV Für Alle | TV Movie | TV Spielfilm |
|---|---|---|---|
| Description | yes | no | yes (fetched from the programme's page) |
| Subtitle | yes | yes | yes (from the page) |
| Year | yes | yes | yes, with country |
| Picture | yes | yes | yes |
| Trailer | no | no | when the page has one |
| NEU badge | no | no | yes |

An empty description means the source did not deliver one, not that something failed.

For TV Spielfilm the details are fetched from the programme's own web page when you open the screen (or earlier, in the background, for the
programmes visible in the grid).

## Keys

| Key | Action |
|---|---|
| **OK**, **YELLOW** | Play the trailer |
| **RED**, **EXIT** | Back |
| **UP**, **LEFT** | Description page up |
| **DOWN**, **RIGHT** | Description page down |

## The trailer

Programmes on TV Spielfilm can have a short video. When there is one, the yellow button is labelled **Trailer**; otherwise the button is
hidden and **OK** does nothing. The video is played as a stream with the standard Enigma2 movie player, with the info bar switched off.
Stopping the player returns you to the details. Only video addresses that end in `mp4` are played.

The trailer is a stream, so it needs the Internet connection while it plays.
