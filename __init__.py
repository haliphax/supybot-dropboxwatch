"""
Add a description of the plugin (to be presented to the user inside the wizard)
here.  This should describe *what* the plugin does.
"""

import supybot
import supybot.world as world

__version__ = ""
__author__ = supybot.Author('haliphax', 'haliphax', 'haliphax@nope')
__contributors__ = {}
__url__ = 'https://github.com/haliphax/supybot-dropboxwatch'

from . import config
from . import plugin
from imp import reload
reload(config)
reload(plugin)

if world.testing:
    from . import test

Class = plugin.Class
configure = config.configure
