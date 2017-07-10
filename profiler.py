
#!/usr/bin/env python
import os
import cProfile
import pstats
os.system('python3 -m cProfile -o profiler.out twostep_test_network.py 40 100 1')
p = pstats.Stats('profiler.out')
#p.strip_dirs().sort_stats(-1).print_stats()
#
#p.sort_stats('name')
#p.print_stats()
p.strip_dirs().sort_stats('cumulative').print_stats(20)
p.strip_dirs().sort_stats('time').print_stats(20)
