# Cache

TVMagazineCockpit keeps what it has downloaded for the current day in a cache folder, so that opening it again, turning pages and looking
at details do not download things twice.

## Where and what

```
/data/TVC/
    2026-10-21/                      <- today's folder (the only one kept)
        events.json                  <- every programme fetched so far
        programpix-<start>-<channel id>.jpg     <- pictures of programmes
```

| File | Content |
|---|---|
| `events.json` | All programmes downloaded today for all days you looked at: a dictionary date -> service reference -> list of programmes. Each programme is the record described in [Architecture](Architecture.md#the-event-record) |
| `programpix-*.jpg` | A programme picture. The name has the programme's start time and the channel id at the current source |

The folder is named after **today's date**.

## When it is filled

| When | What |
|---|---|
| Enigma2 starts | Folders of other days are deleted. If today has no `events.json`, the programmes of all channels of the bouquet are downloaded for today. Then the pictures of the 20:15 programmes are downloaded in a background thread |
| You open a page or a day with missing data | The missing channels are downloaded, merged into `events.json` and saved |
| A picture is shown | Downloaded on first use if it is not in the folder yet |

`events.json` is read when the plugin opens. It is written after each download.

## When it is emptied

- Each start deletes the folders of all other days. So the cache is at most a day old.
- Changing the data source in the settings deletes the whole `/data/TVC` and starts again.
- You can delete `/data/TVC` yourself at any time. It is rebuilt on the next use.

## Size

The pictures dominate. On a test box with TV Spielfilm as the source, the folder for one day was about 16 MB: an `events.json` of
458 KB and 20 pictures between 86 KB and 1.6 MB each. More pictures are added as you browse, so plan for some tens of megabytes
per day.

## Notes

- The cache folder holds only data of **one** data source at a time. The file does not record which source produced it. That is why changing the source
  deletes the cache.
- The programmes of other days are stored in today's folder too. When the date changes, they go with it.
- The detail fetches of TV Spielfilm update the programmes in memory. They reach the file with the next save, which happens after the next
  download of programmes.
