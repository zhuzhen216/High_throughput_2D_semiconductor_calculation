
# coding: utf-8

# In[1]:

#!/usr/bin/env python


# In[2]:

import os
import socket


# In[11]:

def submit():
    hostname=socket.gethostname()
    # list of submission system
    sub_sys = {'guild': 'PBS',
               'comet': 'SLURM',
               'stampede': 'SLURM',
               'cori': 'PBS',
               'edison': 'PBS',
               'optiplex': 'BS',
                }
    if sub_sys[hostname] == 'SLURM':
      os.system ( "qsub submit.sh" )
    if sub_sys[hostname] == 'PBS':
      os.system ( "qsub submit.sh" )


# In[12]:

submit()


# In[ ]:



