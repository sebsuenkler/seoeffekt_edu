#script to delete unassigned results

#include libs
import sys
sys.path.insert(0, '..')
from include import *

Studies.deleteunassignedResults()
