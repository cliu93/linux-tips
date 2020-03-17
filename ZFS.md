# Table of Contents
- [Check ARC Usage](ZFS.md#check-arc-usage)
- [Check ARC Stat](ZFS.md#check-arc-stat)
- [Check ARC Summary](ZFS.md#check-arc-summary)
- [Flush File System Buffer](ZFS.md#flush-the-file-system-buffer)

# Check ARC usage
```bash
# cat /proc/spl/kstat/zfs/arcstats |egrep "dnode_size|arc_dnode_limit|arc_meta_used|arc_meta_limit"
arc_meta_used                   4    6309595080
arc_meta_limit                  4    6309467136
```

# Check ARC stat
```bash
# arcstat.py 1 10
    time  read  miss  miss%  dmis  dm%  pmis  pm%  mmis  mm%  arcsz     c
15:12:52    14     1      7     1   16     0    0     1    7   5.9G  7.8G
15:12:53   21K   699      3   621    3    78    2   695    3   5.9G  7.8G
15:12:54   13K   308      2   205    2   103    2   298    2   5.9G  7.8G
15:12:55   20K   377      1   220    1   157    6   359    1   5.9G  7.8G
15:12:56   12K   188      1   169    1    19   67   182    1   5.9G  7.8G
15:12:57   19K   255      1   227    1    28   56   249    1   5.9G  7.8G
15:12:58   20K   222      1   168    0    54   56   215    1   5.9G  7.8G
15:12:59   20K   274      1   228    1    46    9   180    0   5.9G  7.8G
15:13:00   17K   170      0   138    0    32    6   163    0   5.9G  7.8G
15:13:01   13K   321      2   194    1   127   89   317    2   5.9G  7.8G
```

# Check ARC Summary
```bash
# arc_summary.py

------------------------------------------------------------------------
ZFS Subsystem Report                            Tue Jul 16 15:07:30 2019
ARC Summary: (HEALTHY)
        Memory Throttle Count:                  0

ARC Misc:
        Deleted:                                26.02m
        Mutex Misses:                           347.32k
        Evict Skips:                            347.32k

ARC Size:                               92.16%  7.22    GiB
        Target Size: (Adaptive)         100.00% 7.83    GiB
        Min Size (Hard Limit):          0.40%   32.00   MiB
        Max Size (High Water):          250:1   7.83    GiB

ARC Size Breakdown:
        Recently Used Cache Size:       93.75%  7.35    GiB
        Frequently Used Cache Size:     6.25%   501.45  MiB

ARC Hash Breakdown:
        Elements Max:                           758.80k
        Elements Current:               95.75%  726.56k
        Collisions:                             5.61m
        Chain Max:                              6
        Chains:                                 100.94k

ARC Total accesses:                                     2.08b
        Cache Hit Ratio:                95.11%  1.98b
        Cache Miss Ratio:               4.89%   101.67m
        Actual Hit Ratio:               39.91%  829.15m

        Data Demand Efficiency:         76.05%  7.32m
        Data Prefetch Efficiency:       11.21%  2.35m

        CACHE HITS BY CACHE LIST:
          Anonymously Used:             57.39%  1.13b
          Most Recently Used:           2.84%   56.08m
          Most Frequently Used:         39.12%  773.07m
          Most Recently Used Ghost:     0.63%   12.50m
          Most Frequently Used Ghost:   0.02%   392.74k

        CACHE HITS BY DATA TYPE:
          Demand Data:                  0.28%   5.57m
          Prefetch Data:                0.01%   262.90k
          Demand Metadata:              41.65%  822.99m
          Prefetch Metadata:            58.06%  1.15b

        CACHE MISSES BY DATA TYPE:
          Demand Data:                  1.73%   1.75m
          Prefetch Data:                2.05%   2.08m
          Demand Metadata:              70.38%  71.56m
          Prefetch Metadata:            25.85%  26.28m


File-Level Prefetch: (HEALTHY)
DMU Efficiency:                                 5.08b
        Hit Ratio:                      45.62%  2.32b
        Miss Ratio:                     54.38%  2.76b

        Colinear:                               2.76b
          Hit Ratio:                    0.00%   40.97k
          Miss Ratio:                   100.00% 2.76b

        Stride:                                 2.27b
          Hit Ratio:                    100.00% 2.27b
          Miss Ratio:                   0.00%   113.35k

DMU Misc:
        Reclaim:                                2.76b
          Successes:                    0.04%   1.01m
          Failures:                     99.96%  2.76b

        Streams:                                46.67m
          +Resets:                      0.03%   12.81k
          -Resets:                      99.97%  46.66m
          Bogus:                                0
......
```

# Flush the file system buffer

```bash
Clear PageCache only. 
# sync; echo 1 > /proc/sys/vm/drop_caches

Clear dentries and inodes. 
# sync; echo 2 > /proc/sys/vm/drop_caches

Clear PageCache, dentries and inodes. 
# sync; echo 3 > /proc/sys/vm/drop_caches
```

# txg_sync, z_null_iss and txg_quiesce freezes
```bash
echo 1073741824 >> /sys/module/zfs/parameters/zfs_arc_min
Added to the file /etc/modprobe.d/zfs.conf:

options zfs zfs_arc_max=8589934592
options zfs zfs_arc_min=1073741824
options zfs zfs_prefetch_disable=1
```
