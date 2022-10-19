import json
from operator import itemgetter


def setDiskUsageGrain():
    usageStats = __salt__["disk.usage"]()
    __salt__["grains.setval"]("diskUsage", usageStats)
    return usageStats


def setHostUsageMetrics():
    cpustats = __salt__["status.cpustats"]()
    memstats = __salt__["status.meminfo"]()
    __salt__["grains.setval"]("cpuUsage", cpustats)
    __salt__["grains.setval"]("memUsage", memstats)
    return True
