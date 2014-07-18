import subprocess
import datetime 
from utils import CommandRunner
import re
import time
import smtplib
import os
from random import randrange

from utils import CommandRunner

#subprocess.Popen("env > /tmp/env.output"+str(randrange(500)), shell=True)


cr = CommandRunner() 

#check = cr.run_command("env | grep OS_REGION_NAME","done check")

#print "check['output'] is: %s"% check['output']
#subprocess.Popen(str(check['output'])+" > /tmp/env.output"+str(randrange(500)), shell=True)


region_name = os.environ['OS_REGION_NAME'].rstrip()
print "Performing Ceilometed Tests for Region: "+str(region_name)

#subprocess.Popen("echo "+region_name+" > /tmp/env.output"+str(randrange(500)), shell=True)


start_time = time.time()

""" ************************* Ceilometer Metering API commands ************************************ """

resource_output = cr.run_command("ceilometer resource-list","done resource-list")

meter_name_output = cr.run_command("ceilometer meter-name-list","done meter-name-list")

meter_output = cr.run_command("ceilometer meter-list | awk '{print $2, $8}'","done meter-list")


number_meters_output = cr.run_command("ceilometer meter-list | wc -l","fetched the number of meters")

meter_output_list = re.split('\n', meter_output['output'])

full_meter_list = filter(lambda x:x != " ", meter_output_list)
full_meter_list = filter(lambda x:x != "", full_meter_list)
full_meter_list = filter(lambda x:x != "Name Resource", full_meter_list)


sample_run_time_list = []
start_sample_time = time.time()
for i in range(len(full_meter_list)):
    meter_rscID_split = full_meter_list[i].split(' ',1)
    sample_output = cr.run_command("ceilometer sample-list -m "+meter_rscID_split[0]+" -q resource_id="+meter_rscID_split[1],"done sample-list")
    sample_run_time_list.append(sample_output['runTime'])
    
end_sample_time = time.time()
sample_run_time = end_sample_time - start_sample_time

ind_sample_runTime = cr.getStats(sample_run_time_list,"Sample List")

stats_run_time_list = []
start_stats_time = time.time()    
for i in range(len(full_meter_list)):
    meter_rscID_split = full_meter_list[i].split(' ',1)
    statistics_output = cr.run_command("ceilometer statistics -m "+meter_rscID_split[0]+" -q resource_id="+meter_rscID_split[1],"done statistics")
    stats_run_time_list.append(statistics_output['runTime'])

end_stats_time = time.time()
stats_run_time = end_stats_time - start_stats_time

ind_stats_runTime = cr.getStats(stats_run_time_list,"Statistics List")

""" ************************* Ceilometer Alarm API commands ************************************ """

alarmCr_output = cr.run_command("~/devstack/./savi-alarm-create-test.sh","Created Alarm")

alarmList_output = cr.run_command("ceilometer alarm-list | grep -e '| [0-9a-f]' | awk '{print $2}'","Fetched Alarm IDs")

alarmShow_output = cr.run_command("ceilometer alarm-show -a "+alarmList_output['output'],"Fetched Alarm Info")

alarmUpd_output = cr.run_command("ceilometer alarm-update --threshold 90 --period 2 -a "+alarmList_output['output'],"Updated Alarm")

alarmHist_output = cr.run_command("ceilometer alarm-history -a "+alarmList_output['output'],"Fetched Alarm History")

alarmDel_output = cr.run_command("ceilometer alarm-delete -a "+alarmList_output['output'],"Deleted Alarm")

""" ************************* Send Email ******************************************************* """

from_addr='from email address'
addr_pwd='email address password'
send_addr_array = ['email addresses to send']

end_time=time.time()

total_runTime = end_time - start_time

#check = cr.run_command("env | grep OS","done check")

#subprocess.Popen(str(check['output'])+" > /tmp/env.output"+str(randrange(500)), shell=True)

for i in send_addr_array:

    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(from_addr, addr_pwd)
    header = 'To:' + i + '\n' + 'From: ' + from_addr + '\n' + 'Subject:Automated Ceilometer Tests for Region: '+region_name+' \n'
    msg = header +'\n' 
    info = 'Ceilometer Resource-List Running time: '+str(resource_output['runTime'])+' seconds. \n'
    info = info + 'Ceilometer Meter-Name-List Running time: '+str(meter_name_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Meter List Running time: '+str(meter_output['runTime'])+' seconds.\n'
    info = info + 'Total Number of Meters in this Region: '+str(number_meters_output['output'])
    info = info + '-------------------------------------------------------------------------------------------\n'
    info = info + 'Ceilometer Average Sample List Runing time: '+str(ind_sample_runTime['avg_val'])+' seconds.\n'
    info = info + 'Ceilometer Minimum Sample List Runing time: '+str(ind_sample_runTime['min_val'])+' seconds.\n'
    info = info + 'Ceilometer Maximum Sample List Runing time: '+str(ind_sample_runTime['max_val'])+' seconds.\n'
    info = info + 'Ceilometer Total Sample List Running time: '+str(round(sample_run_time,3))+' seconds.\n'
    info = info + '-------------------------------------------------------------------------------------------\n'
    info = info + 'Ceilometer Average Statistics List Runing time: '+str(ind_stats_runTime['avg_val'])+' seconds.\n'
    info = info + 'Ceilometer Minimum Statistics List Runing time: '+str(ind_stats_runTime['min_val'])+' seconds.\n'
    info = info + 'Ceilometer Maximum Statistics List Runing time: '+str(ind_stats_runTime['max_val'])+' seconds.\n'
    info = info + 'Ceilometer Total Statistics List Running time: '+str(round(stats_run_time,3))+' seconds.\n'
    info = info + '-------------------------------------------------------------------------------------------\n'
    info = info + 'Ceilometer Alarm Create Running time: '+str(alarmCr_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Alarm List Running time: '+str(alarmList_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Alarm Show Running time: '+str(alarmShow_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Alarm Update Running time: '+str(alarmUpd_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Alarm History Running time: '+str(alarmHist_output['runTime'])+' seconds.\n'
    info = info + 'Ceilometer Alarm Delete Running time: '+str(alarmDel_output['runTime'])+' seconds.\n'
    info = info + '-------------------------------------------------------------------------------------------\n'
    info = info + 'Total Run Time: '+str(round(total_runTime,3))+' seconds.\n'
    #info = info + 'Environment variables: '+str(check['output'])+'\n'
    msg = msg + info     
    
    try: 
        smtpserver.sendmail(from_addr, i, msg)
        smtpserver.close()
        print "Successfully sent email to user %s"% i
    except RuntimeError as e:
        print "Failed to send email to user, Reason: %s"% e

