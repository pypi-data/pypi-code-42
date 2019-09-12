import os

import pandas as pd

from IPython.core.magic import (
    Magics, magics_class, cell_magic)
from IPython.core.magic_arguments import (
    argument, magic_arguments, parse_argstring)


def write_data(fname, data):
    data.to_csv(fname, index=False)


def load_data(fname):
    return pd.read_csv(fname)


@magics_class
class PDCache(Magics):
    @magic_arguments()
    @argument(
        'variable', type=str,
        help='Variable to be cached.'
    )
    @argument(
        'fname', type=str,
        help='File which variable is saved in.'
    )
    @cell_magic
    def pdcache(self, line, cell):
        """Cache variables to file."""
        ip = self.shell
        args = parse_argstring(self.pdcache, line)

        if os.path.exists(args.fname):
            # load cached data
            print('Loading data from cache')
            data = load_data(args.fname)
            ip.push({
                args.variable: data
            })
        else:
            # execute and cache data
            ip.run_cell(cell)

            print('Caching new data')
            data = ip.user_ns[args.variable]
            write_data(args.fname, data)
