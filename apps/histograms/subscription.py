from ariadne import SubscriptionType

import asyncio
import numpy as np

subscription = SubscriptionType()

""" Asynchronous generator
"""

SUB_SLEEP_TIME = 1  # [seconds] to wait in between subscription calls

from .query import _filter_histograms, _get_latest_hist_table_entry


@subscription.source("getLiveHistograms")
async def source_live_histograms(obj, info):
    while True:
        await asyncio.sleep(SUB_SLEEP_TIME)
        histograms = await _filter_histograms(ids=None, names=None, types=None, minDate=None, maxDate=None, isLive=True)
        lastRun = await _get_latest_hist_table_entry()
        if histograms:
            for i, hist in enumerate(histograms):
                if hist.data:
                    hist.current = hist.data[-1]
            yield {"histograms": histograms, "lastRun": lastRun.name}
        else:
            yield {"histograms": None, "lastRun": lastRun.name}


"""
Subscription
"""


@subscription.field("getLiveHistograms")
def resolve_live_histograms(histograms, info):
    return histograms
