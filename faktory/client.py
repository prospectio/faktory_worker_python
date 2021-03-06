import uuid
import collections

from ._proto import Connection


class Client:
    is_connected = False

    def __init__(self, faktory=None, connection=None):
        self.faktory = connection or Connection(faktory)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        self.is_connected = self.faktory.connect()
        return self.is_connected

    def disconnect(self):
        self.faktory.disconnect()
        self.is_connected = False

    def queue(self, task, args=None, queue='default', priority=5, jid=None, custom=None, reserve_for=None, at=None, retry=5):
        was_connected = self.is_connected
        if not self.is_connected:
            # connect if we are not already connected
            self.connect()

        if not task:
            raise ValueError("Empty task name")

        if not queue:
            raise ValueError("Empty queue name")

        if not jid:
            jid = self.random_job_id()

        if args is None:
            args = ()

        request = {
            'jid': jid,
            'queue': queue,
            'jobtype': task,
            'priority': priority
        }

        if custom is not None:
            request['custom'] = custom

        if args is not None:
            if not isinstance(args, (collections.Iterable, set, list, tuple)):
                raise ValueError("Argument `args` must be an iterator, generator, list, tuple or a set")

            request['args'] = list(args)

        if reserve_for is not None:
            request['reserve_for'] = reserve_for

        if at is not None:
            request['at'] = at

        request['retry'] = retry

        self.faktory.reply("PUSH", request)
        ok = next(self.faktory.get_message())

        if not was_connected:
            self.disconnect()

        return ok == "OK"

    def random_job_id(self):
        return uuid.uuid4().hex
