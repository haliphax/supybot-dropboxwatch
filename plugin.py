from enum import Enum
from hashlib import sha256
import hmac
from multiprocessing import Queue
from time import time

from supybot.commands import *
import supybot.callbacks as callbacks
import supybot.conf as conf
import supybot.httpserver as httpserver
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.log as log
import supybot.plugins as plugins
import supybot.schedule as schedule
import supybot.utils as utils

from dropbox import Dropbox
from dropbox.files import DeletedMetadata


class EventType(Enum):
    update = 1
    delete = 2


class DropboxWatchServerCallback(httpserver.SupyHTTPServerCallback):
    name = 'DropboxWatch'
    _dbx = Dropbox(conf.supybot.plugins.DropboxWatch.apiKey())

    def __init__(self):
        super(DropboxWatchServerCallback, self).__init__()
        self._cursor = self._dbx.files_list_folder_get_latest_cursor(
            '', recursive=True).cursor

    def doGet(self, handler, path):
        handler.send_response(200)
        handler.send_header('Content-Type', 'text/plain')
        handler.send_header('X-Content-Type-Options', 'nosniff')
        handler.end_headers()
        handler.wfile.write(path.replace('/?challenge=', '').encode('utf-8'))

    def doPost(self, handler, path, form):
        signature = handler.headers['X-Dropbox-Signature']

        if not hmac.compare_digest(signature,
                                   hmac.new((conf.supybot.plugins.DropboxWatch
                                             .appSecret().encode('utf-8')),
                                            form, sha256).hexdigest()):
            handler.send_response(403)
            log.warning('Invalid Dropbox signature: %s\n\t%s' % (
                signature, str(form)))
            handler.wfile.write('Invalid signature'.encode('utf-8'))
            return

        handler.send_response(200)
        result = self._dbx.files_list_folder_continue(self._cursor)
        self._cursor = result.cursor

        for entry in result.entries:
            log.info('DropboxWatch update: %s' % str(entry))

            if type(entry) is DeletedMetadata:
                events.put_nowait((EventType.delete, entry.path_display))
            else:
                events.put_nowait((EventType.update, entry.path_display))


class DropboxWatch(callbacks.Plugin):

    def __init__(self, irc):
        self.__parent = super(DropboxWatch, self)
        self.__parent.__init__(irc)
        callback = DropboxWatchServerCallback()
        self._abbrev = DropboxWatchServerCallback.name.lower()

        for server in httpserver.http_servers:
            if self._abbrev in server.callbacks:
                httpserver.unhook(self._abbrev)
                break

        httpserver.hook(self._abbrev, callback)
        interval = conf.supybot.plugins.DropboxWatch.interval()

        def f():
            if events.empty():
                return

            path_dict = dict()

            for channel in irc.state.channels:
                paths = conf.supybot.plugins.DropboxWatch.paths.get(channel)()

                if len(paths) == 0:
                    continue

                for path in paths:
                    if path in path_dict:
                        continue

                    path_dict[path] = (set(), set())

            try:
                while not events.empty():
                    event = events.get_nowait()

                    for path in path_dict.keys():
                        if event[1].startswith('/' + path):
                            updates, deletes = path_dict[path]

                            if event[0] == EventType.delete:
                                deletes.add(event[1])
                            else:
                                updates.add(event[1])

                            path_dict[path] = (updates, deletes)
            except Queue.Empty:
                log.warning('Queue empty')

            for k in path_dict.keys():
                updates, deletes = path_dict[k]
                output = ''

                if len(deletes) > 0:
                    output = 'Deleted: %s' % (', '.join(deletes))

                if len(updates) > 0:
                    if len(output) > 0:
                        output += ' | '

                    output += 'Updated: %s' % (', '.join(updates))

                if len(output) == 0:
                    continue

                output = '[Dropbox] %s' % output

                for chan in irc.state.channels:
                    paths = conf.supybot.plugins.DropboxWatch.paths.get(chan)()

                    if len(paths) == 0 or k not in paths:
                        continue

                    log.info('%s >> %s' % (chan, output))
                    irc.queueMsg(ircmsgs.privmsg(chan, output))

        if self._abbrev in schedule.schedule.events:
            schedule.removeEvent(self._abbrev)

        schedule.addPeriodicEvent(f, interval, name=self._abbrev, now=False)

    def die(self):
        self.__parent.die()

        for server in httpserver.http_servers:
            if self._abbrev in server.callbacks:
                httpserver.unhook(self._abbrev)
                break

        if self._abbrev in schedule.schedule.events:
            schedule.removeEvent(self._abbrev)


Class = DropboxWatch
events = Queue()
