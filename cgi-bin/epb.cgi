import sys
sys.path.append('../vendor')

import EPB
import wsgiref.handlers
wsgiref.handlers.CGIHandler().run(EPB.app)
