#!/bin/bash

while :
    do
        alarm_id=`ceilometer alarm-list | grep -e '| [0-9a-f]' | awk '{print $2}'`
        IFS=$'\n'
        set -- $alarm_id
        number_alarms=$#

        if [ $number_alarms -gt 0 ]; then
            ceilometer alarm-delete -a $1
            echo "Deleted Alarm with Alarm ID: $1"
        else
            break

        fi
    done

    echo "Finished deleting all the alarms! To verify, the alarm-list is shown below:"
    ceilometer alarm-list


