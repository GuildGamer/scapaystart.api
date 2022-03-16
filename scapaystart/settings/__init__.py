from .base import *

if DEBUG == True:
    from .dev import *

elif DEBUG == False:
    from .prod import *
