from . import captcha  # noqa
from . import circus  # noqa
from . import defragmentation  # noqa
from . import generators  # noqa
from . import hash  # noqa
from . import hexed  # noqa
from . import passphrase  # noqa
from . import plumber  # noqa
from . import reallocation  # noqa
from . import registers  # noqa
from . import scanner  # noqa
from . import spiral  # noqa
from . import stream  # noqa
from . import trampolines  # noqa


BY_DAY_NUMBER = {
    1: captcha,
    2: None,
    3: spiral,
    4: passphrase,
    5: trampolines,
    6: reallocation,
    7: circus,
    8: registers,
    9: stream,
    10: hash,
    11: hexed,
    12: plumber,
    13: scanner,
    14: defragmentation,
    15: generators,
}
