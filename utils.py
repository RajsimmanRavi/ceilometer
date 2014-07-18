import subprocess
import re
import datetime
import time
from random import randrange
import struct

class CommandRunner(object):

    def run_command(self,command, done_phrase):
        print command
        start_time = time.time()
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        #p.wait()
        end_time = time.time()
        run_time = end_time - start_time
        print out
        print done_phrase
        return_output = {'output': out, 'runTime': round(run_time,3)}
        print "---------------------------------------\n"
        return return_output

    def getStats(self,data_list,which_data):
        print "Getting statistics for "+ which_data +"..."
        #subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)
        
        min_val = min(data_list)
        #subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)

        max_val = max(data_list)
        
        #subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)

        avg_val = sum(data_list)/float(len(data_list))
        
        #subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)

        return_output = {'min_val':min_val,'max_val':max_val,'avg_val':round(avg_val,3)}
        #subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)
        return return_output

        
