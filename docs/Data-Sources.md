# Data Sources

TVMagazineCockpit has no programme data of its own. It reads three public TV-magazine websites. You choose one in the
[settings](Settings.md#data-source). The sources differ in how much they deliver.

| | TV Für Alle (`tvfa`) | TV Movie (`tvm`) | TV Spielfilm (`tvs`) |
|---|---|---|---|
| Website | tvfueralle.de | tvmovie.de | tvspielfilm.de |
| Default | yes | | |
| Programme list per channel | all channels in one answer | one request per channel (up to 50 entries) | two page requests per channel |
| Description | long text | none | from the programme's own page |
| Subtitle / episode title | yes | yes | from the page |
| Year | yes | yes | year, with country |
| Category, genre | no | yes | yes (from the list) |
| Picture | yes | yes | yes (from the page) |
| Trailer | no | no | when the page has one |
| NEU badge | no | no | yes |
| Details loaded per programme | no | no | yes, one page each |

The ids that identify a channel at each source are in the [channel dictionary](Channels.md).

## Which to choose

- **TV Für Alle** is the lightest: one request per day for all channels. Good for a quick overview. It has descriptions
  and pictures but no trailers.
- **TV Movie** gives categories and genres, but no description in the details.
- **TV Spielfilm** gives the most (description, trailer, NEU badge) at the price of many more requests: two list pages per channel, and
  one detail page per programme you look at.

## What is requested, and when

| Source | List | Detail |
|---|---|---|
| TV Für Alle | `https://tvfueralle.de/api/broadcasts/<date>` | none |
| TV Movie | `https://proxy.xceler8.io/v2/epg-search?channelId=<id>&airTime=<date>T04:00:00.000Z&limit=50` (with the `Referer` of tvmovie.de) | none; pictures from `images.tvmovie.de` |
| TV Spielfilm | `https://www.tvspielfilm.de/tv-programm/sendungen/?channel=<id>&date=<date>&page=1` and `&page=2` | the programme's own page |

Requests are made by a background thread, never by the screen itself, so the box stays responsive while data loads.
Everything downloaded for the day is kept in the [cache](Cache.md); nothing is requested twice.

## Reliability

- TV Für Alle and TV Movie use JSON interfaces, which change rarely.
- TV Spielfilm is read by **parsing the HTML** of the pages. If the site changes its layout, programmes or details may be missing
  until the plugin is updated. If that happens, switch to another source in the settings.
- All three depend on third-party websites. A site can be unavailable, change its terms, or block requests.

## Time zones

Times from the sources are converted to your box's local time.

## Changing the source

In the settings (**MENU**). After saving, the plugin clears the screen, deletes the cache folder (`/data/TVC`, because the programmes of the old source
cannot be reused), and loads the new source. A channel that the new source has no id for disappears from the pages
(see [Channels](Channels.md)).
