# Troubleshooting

## Logging

Lines of this plugin in the Enigma2 debug log (usually `/home/root/logs/Enigma2_debug_*.log`) start with `TVC:`. Set *Log level* to
`DEBUG` in the settings (expert mode) to see the requests, the parsed programmes and the cache steps. `DEBUG` is very verbose; set it
back to `INFO` afterwards.

## The title bar says "No event data available"

None of the six channels on the page has data for that day.

| Check | What to do |
|---|---|
| Is the box online? | The data comes from websites. Check that the box can reach the Internet |
| Does the source have data for that day? | Days far ahead may not be published yet. Try another day, or another source |
| Is the source working? | A website can be down or have changed. Switch the *Data source* in the settings |
| Is the channel known to this source? | A channel without an id for the source has no data. See [Channels](Channels.md) |

## A channel is missing from the pages

It must be in the bouquet, in the channel dictionary with a name, and have an id for the chosen source. See
[Channels](Channels.md#which-channels-appear). The quickest check is to switch to another source: if the channel shows up there, the first
source has no id for it.

## The whole list is empty or has few channels

- The *Bouquet* setting may point to a bouquet you did not expect. In *Auto* mode it is the bouquet you last used in the channel list.
- Your channels may have service references that differ from the delivered dictionary (another satellite position, another provider). Make
  your own `/etc/enigma2/tvc_channel_dict.json` with your references.
- The `Services:` count in the title bar tells you how many channels passed all the checks.

## Programme times look wrong

Times are converted to the box's local time. Check Enigma2's time zone setting. If only one channel is off, the source has wrong data for it.

## No pictures

- The first picture of a programme is downloaded when it is first shown and appears a moment later.
- Picons (channel logos) are separate from programme pictures. They come from Enigma2's picon folder. If they are missing, fix that in Enigma2; the plugin's
  own *Picon directory* setting is not used.
- Not every programme has a picture at every source.

## No description

TV Movie does not deliver descriptions. Use TV Für Alle or TV Spielfilm for those. See [Data Sources](Data-Sources.md).

## No trailer, no NEU badge

Both come only from TV Spielfilm, and only for programmes where the programme page offers them.

## The grid feels slow when I open a page

With TV Spielfilm the first view of a page makes two list requests per channel and then one detail request per visible programme. TV Für Alle
makes a single request per day. Start-up downloads today's data in advance; if the box was off or offline at start-up, that work happens when you open
the plugin.

## Start fresh

Delete the folder `/data/TVC` and reopen the plugin. Changing the data source in the settings also deletes it. It is rebuilt on the next use.

## The trailer does not start

The details screen offers it only for programmes with a video address that ends in `mp4`. The stream also needs to be reachable from the box.

## Limitations

- **Third-party websites.** Everything depends on them. TV Spielfilm is read by parsing HTML and breaks when the site changes.
- **German-language offer.** The sources and the delivered channel dictionary are for German-language TV.
- **The channel dictionary is line-up specific.** See [Channels](Channels.md).
- **One source at a time**, and changing it clears the cache.
- **Up and down are limited** inside a column: you cannot select the first programme of the day, and the grid shows five rows.
- **The "Picon directory" setting has no effect.** Picons come from Enigma2.
- **The bouquet name in the title bar** is only updated when you reopen the plugin.
