# Channels

## Which channels appear

A channel appears in the grid only if **all** of these are true:

1. It is in the **bouquet** that the plugin uses (see [Settings](Settings.md#bouquet)). Markers (the dividers in a bouquet) are ignored.
2. It has an entry in the **channel dictionary** (below), with a name.
3. That entry has an id for the **data source** you chose.

The channels of the bouquet that pass are listed in bouquet order, six per page. If a channel you expect is missing, one of these
three is the reason. The title bar's `Services:` count is the number of channels that passed.

## The channel dictionary

The plugin does not guess which website channel belongs to which of your channels. A file, `tvc_channel_dict.json`, says so. It maps the
**service reference** of a channel on your box to the channel's name and its ids at the three sources:

```json
{
  "1:0:19:2855:401:1:C00000:0:0:0:": {
    "tvs_id": "BR",
    "name": "BR Sued",
    "tvfa_id": 13,
    "tvm_id": "5",
    "tvh_id": "51"
  }
}
```

| Key | Meaning |
|---|---|
| (the object name) | The service reference as Enigma2 writes it, including the trailing colon |
| `name` | The channel name shown in the column header |
| `tvs_id` | Channel code at TV Spielfilm (the `channel=` value in its address) |
| `tvm_id` | Channel id at TV Movie |
| `tvfa_id` | Channel number at TV Für Alle |
| `tvh_id` | Channel id at HÖRZU. Stored for other Cockpit plugins; TVMagazineCockpit does not use it |

A channel needs only the ids of the sources you use. The delivered dictionary has about 240 channels. Many have all ids; some,
for example pay-TV channels, only have `tvs_id`.

### Which file is used

The plugin looks for `tvc_channel_dict.json` in two places and uses the **first one found**:

1. `/etc/enigma2/tvc_channel_dict.json` (your own copy)
2. the plugin folder (the delivered one)

The delivered file holds the references of one particular satellite and cable line-up. If your references differ (another satellite
position, a different provider, a channel that has been renumbered), the channel is not recognised.

### Adding or fixing a channel

1. Copy the delivered file to `/etc/enigma2/tvc_channel_dict.json` (once). From then on your copy replaces the delivered one,
   which means it is not updated by plugin updates; keep it in step by hand.
2. Find the service reference of your channel (the channel list's info, or `/etc/enigma2/lamedb` / the bouquet file).
3. Add an entry, or change the key of an existing one to your reference. Fill in `name` and at least the id for your source.
4. Press **0** in the plugin to reload the dictionary.

To find the id of a channel at a source, look at the source website: the TV Spielfilm program page for a channel has the channel code in its address
(`...?channel=ARD`). TV Für Alle and TV Movie use numbers that appear in their data.

## Master list

`channels/master_channels.json` is a larger reference list that is installed with the plugin. It lists channels with their names and ids
at the sources and the service references known for each. The plugin itself does not read it; the script
`test/channels/create_dict.py` in the repository uses it to generate `tvc_channel_dict.json`.
