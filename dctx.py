#
# DCT reports

import os
from helpers import *

#
# Main dctx logic
#
rp = source_list()
rp = source_search("ASE")
quit()

rp = dsource_list()
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
