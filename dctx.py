#
# DCT reports

import os

from sources import *
from dsources import *
from jobs import *
from vdbgroups import *
from vdbs import *
from reports import *
from environments import *


#
# Main dctx logic
#

rp = dsource_list()
print(rp)

rp = source_by_id("1-APPDATA_SOURCE_CONFIG-177")
print(rp)
rp = source_list()
print(rp)
rp = source_search("ASE")
print(rp)
quit()

#rp = environment_list()
#rp = environment_by_id("1-UNIX_HOST_ENVIRONMENT-41")
#rp = environment_operation("1-UNIX_HOST_ENVIRONMENT-41","disable")
js = job_status_by_id("d3bc4852c98345549a030903ecb6d713")
content_formatter(js)
#job_monitor("d3bc4852c98345549a030903ecb6d713")

quit()


rp = vdbgroup_search("231")
quit()

rp = dsource_search("231")
quit()
rp = vdb_search("MySQL")
quit()

rp = environment_search("MuSQL")
quit()

rp = engine_register("CDE99","10.160.1.99","admin","Delphix_123!")
quit()




rp = engine_list()
rp = vdb_list()
rp = vdbgroup_list()
rp = dsource_list()
rp = environment_list()




rp = report_api_usage('2022-09-29T15:00:00-04:00','2022-10-10T15:10:00-04:00' )

print("\n")

rp = report_storage_summary()

print("\n")

rp = report_vdb_inventory()

print("\n")

rp = report_dsource_usage()
