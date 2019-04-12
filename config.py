import supybot.conf as conf
import supybot.registry as registry


def configure(advanced):
    conf.registerPlugin('DropboxWatch', True)


DropboxWatch = conf.registerPlugin('DropboxWatch')
conf.registerGlobalValue(DropboxWatch, 'apiKey',
                         registry.String('', """The Dropbox API key""",
                                         private=True))
conf.registerChannelValue(DropboxWatch, 'paths',
                          registry.SpaceSeparatedListOfStrings('',
                              """The list of paths to announce"""))
