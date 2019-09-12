
import numpy as np
from collections import namedtuple
from json import loads
from logging import getLogger

from . import MultiProcCalculator, ActivityJournalCalculatorMixin, DataFrameCalculatorMixin
from ..names import FTHR, HEART_RATE, HR_ZONE
from ...data.frame import activity_statistics, statistics
from ...data.impulse import hr_zone, impulse_10
from ...squeal import Constant, StatisticJournalFloat

log = getLogger(__name__)

# constraint comes from constant
HRImpulse = namedtuple('HRImpulse', 'dest_name, gamma, zero, one, max_secs')


class ImpulseCalculator(ActivityJournalCalculatorMixin, DataFrameCalculatorMixin, MultiProcCalculator):

    def __init__(self, *args, impulse_ref=None, **kargs):
        self.impulse_ref = self._assert('impulse_ref', impulse_ref)
        super().__init__(*args, **kargs)

    def _startup(self, s):
        self.impulse = HRImpulse(**loads(Constant.get(s, self.impulse_ref).at(s).value))
        log.debug('%s: %s' % (self.impulse_ref, self.impulse))

    def _read_dataframe(self, s, ajournal):
        try:
            heart_rate_df = activity_statistics(s, HEART_RATE, activity_journal=ajournal)
            fthr_df = statistics(s, FTHR, constraint=ajournal.activity_group)
            return heart_rate_df, fthr_df
        except Exception as e:
            log.warning(f'Failed to generate statistics for activity: {e}')
            raise

    def _calculate_stats(self, s, source, data):
        heart_rate_df, fthr_df = data
        hr_zone(heart_rate_df, fthr_df)
        impulse_df = impulse_10(heart_rate_df, self.impulse)
        # join so that we can iterate over values in time order
        stats = impulse_df.join(heart_rate_df, how='outer')
        return stats

    def _copy_results(self, s, ajournal, loader, stats):
        for time, row in stats.iterrows():
            if not np.isnan(row[HR_ZONE]):
                loader.add(HR_ZONE, None, None, ajournal.activity_group, ajournal, row[HR_ZONE], time,
                           StatisticJournalFloat)
            if not np.isnan(row[self.impulse.dest_name]):
                loader.add(self.impulse.dest_name, None, None, ajournal.activity_group, ajournal,
                           row[self.impulse.dest_name], time, StatisticJournalFloat)
        # if there are no values, add a single null so we don't re-process
        if not loader:
            loader.add(HR_ZONE, None, None, ajournal.activity_group, ajournal, None, ajournal.start,
                       StatisticJournalFloat)
