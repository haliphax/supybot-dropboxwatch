# supybot/limnoria DropboxWatch plugin

This plugin will watch a Dropbox folder and announce updates to paths that
channels can elect to follow.

## settings

### global

- `supybot.plugins.DropboxWatch.apiKey` (String): The Dropbox OAuth2 API key
- `supybot.plugins.DropboxWatch.interval` (PositiveInteger): The time (in
  seconds) between polling the event queue for announcement notifications
  (default: 60)

To set these, use the `config` command.

*Note: If any of the global settings are changed, the plugin will need to be
reloaded. Currently, there is a bug which causes the HTTP callback to remain
hooked after the plugin has been unloaded, which prevents the HTTP server from
starting back up properly. If this happens, reload the plugin a second time.*

### channel

- `supybot.plugins.DropboxWatch.paths` (SpaceSeparatedListOfStrings): Which
  paths (relative to the root) this channel would like to receive announcements
  for (example: impure73 wip Public)

To set these, use the `config channel` command.
