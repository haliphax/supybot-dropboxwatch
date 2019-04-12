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

### channel

- `supybot.plugins.DropboxWatch.paths` (SpaceSeparatedListOfStrings): Which
  paths (relative to the root) this channel would like to receive announcements
  for (example: impure73 wip Public)

To set these, use the `config channel` command.
