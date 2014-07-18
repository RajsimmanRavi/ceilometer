#!/bin/bash -f

### --- Default Variables --- ###
source ~/devstack/functions_ht

METER_NAME='cpu_util'
STATISTIC_VAL='avg'
COMPARISON_OPERATOR='gt'
THRESHOLD_VAL=40
PERIOD_VAL=30
EVALUATION_PERIODS=1
ALARM_ACTION="log://"

green_desc_title "Creating Alarm"
ceilometer alarm-threshold-create --name TestAlarm$RANDOM --meter-name $METER_NAME --description "Alarm Configuration" --statistic $STATISTIC_VAL --comparison-operator $COMPARISON_OPERATOR --threshold $THRESHOLD_VAL --period $PERIOD_VAL --evaluation-periods $EVALUATION_PERIODS --alarm-action $ALARM_ACTION
