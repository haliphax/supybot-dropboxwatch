# supybot/limnoria DropboxWatch plugin

This plugin will watch a Dropbox folder and announce updates to paths that
channels can elect to follow.

## settings

### global

- `supybot.plugins.DropboxWatch.apiKey` _(String)_: The Dropbox OAuth2 API key
- `supybot.plugins.DropboxWatch.appSecret` _(String)_: The Dropbox app secret
- `supybot.plugins.DropboxWatch.interval` _(PositiveInteger)_: The time (in
  seconds) between polling the event queue for announcement notifications
  (default: `60`)

To set these, use the `config` command.

*Note: If any of the global settings are changed, the plugin will need to be
reloaded.*

### channel

- `supybot.plugins.DropboxWatch.paths` _(SpaceSeparatedListOfStrings)_: Which
  paths (relative to the root) this channel would like to receive announcements
  for (example: `impure73 wip Public`)

To set these, use the `config channel` command.
