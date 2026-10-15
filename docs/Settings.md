# Settings

Open them with **MENU** inside the plugin. The *Log level* entry is only shown in expert mode.

| Setting | Default | Effect |
|---|---|---|
| Data source | TVFürAlle | Where the programmes come from: TVFürAlle, TVMovie or TVSpielfilm |
| Bouquet | Auto | Which bouquet's channels are shown |
| Picon directory | `/usr/share/enigma2/picon/` | See the note below |
| Log level | INFO | `ERROR`, `INFO`, `DEBUG`. Lines in the Enigma2 debug log start with `TVC:` |

## Data source

See [Data Sources](Data-Sources.md) for what each delivers. After you save a **changed** source, the plugin clears the screen, deletes the
cache and loads the new source's data. Saving without changing the source keeps the cache. If you change only the bouquet, the view is
reloaded.

## Bouquet

| Choice | Meaning |
|---|---|
| **Auto** | The bouquet you last used in Enigma2's channel list |
| A bouquet name | Always that bouquet |

The title bar shows the bouquet's name. It is worked out when the plugin is opened and not updated by a later change in the settings.
In *Auto* mode it is the bouquet that contains the channel you are watching, which can differ from the one used for the columns if you
have navigated the channel list to another bouquet since.

Only TV bouquets are offered. Channels still have to be known to the plugin to appear (see [Channels](Channels.md)).

## Picon directory

The setting is shown but the plugin does not read it. Picons are looked up by Enigma2's own picon mechanism, so they follow Enigma2's picon
settings (the picon path and the names it expects). If picons are missing, fix them in Enigma2, not here.

## Not in the setup screen

| Key | Default | Effect |
|---|---|---|
| `config.plugins.tvmagazinecockpit.temp_dir` | `/data/TVC` | The cache folder. The only choice offered is `/data/TVC` |

## Applying changes

Data source and bouquet changes take effect when you leave the settings with **save**; the plugin reloads by itself. The log level takes effect at once.
