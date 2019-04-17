import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin('DropboxWatch', True)


DropboxWatch = conf.registerPlugin('DropboxWatch')
conf.registerGlobalValue(DropboxWatch, 'apiKey',
                         registry.String('', """The Dropbox API key""",
                                         private=True))
conf.registerGlobalValue(DropboxWatch, 'appSecret',
                         registry.String('', """The Dropbox app secret""",
                                         private=True))
conf.registerGlobalValue(DropboxWatch, 'interval',
                         registry.PositiveInteger(60,
                             """Number of seconds between parsing events"""))
conf.registerChannelValue(DropboxWatch, 'paths',
                          registry.SpaceSeparatedListOfStrings('',
                              """The list of paths to announce"""))
