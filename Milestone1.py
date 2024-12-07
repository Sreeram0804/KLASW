import json

with open('Input/Milestone1.json','r') as file:
    data=json.load(file)

steps_data=data['steps']
machines_data=data['machines']
wafers_data=data['wafers']

print(steps_data)
print()
print(machines_data)
print()
print(wafers_data)

schedule=[]

# time_allocation={}
# for machine in machines_data:
#     time_allocation[machine['machine_id']]=[]

# wafer_allocation={}

# quantity=wafers_data['quantity']

# while(quantity!=0):
#     for machine in machines_data:
#         for wafer in wafers_data:
#             # if(step['id']==machine['step_id']):
#             #     if(step['parameters']['P1'][0]<=machine['initial_parameters'] and step['parameters']['P1'][1]>=machine['initial_parameters']):
#             prev_time=time_allocation[machine['machine_id']]
#             if(len(prev_time)==0):
#                 time_allocation[machine['machine_id']]=[0,wafer['processing_times'][machine['step_id']]]
#             else:
#                 time_allocation[machine['machine_id']]=[prev_time[1],prev_time[1]+wafer['processing_times'][machine['step_id']]]



running={}
finished={}
for machine in machines_data:
    running[machine['machine_id']]=[]

for step in steps_data:
    finished[step['id']]=[]

wafers={}
for wafer in wafers_data:
    type=wafer['type']
    for wafer_num in range(1,wafer['quantity']+1):
        wafers[type+'-'+str(wafer_num)]=wafer['processing_times']


def check(wafer,finished,running):
    for process_wafers in running.values():
        if(wafer in process_wafers):
            return False
    if(wafer in finished):
        return False
    return True

quantity=len(wafers)
time=0
while(True):
    for machine in machines_data:
        if(running[machine['machine_id']]==[]):
            for wafer in wafers:
                if(wafers[wafer][machine['step_id']]!=0 and check(wafer,finished[machine['step_id']],running)):
                    name=wafer
                    running[machine['machine_id']]=[name,time+wafers[wafer][machine['step_id']]]
                    schedule.append({'wafer_id':name,'step':machine['step_id'],'machine':machine['machine_id'],'start_time':time,'end_time':time+wafers[wafer][machine['step_id']]})
                    break
        else:
            if(running[machine['machine_id']][1]-1==time):
                finished[machine['step_id']].append(running[machine['machine_id']][0])
                running[machine['machine_id']]=[]
    time+=1
    # min_time=9999        #Dropped as it skips wafers sometimes if gone directly to the next min value in running
    # for run_time in running.values():
    #     if(len(run_time)!=0):
    #         min_time=min(min_time,run_time[1])
    # if(min_time==9999):
    #     time+=1
    # else:
    #     time+=(min_time-time)-1
    flag=1
    for step in steps_data:
        if(len(finished[step['id']])!=quantity):
            flag=0
            break
    if(flag==1):
        break

print(schedule)

result={'schedule':schedule}
with open('Milestone1Output.json','w') as file:
    json.dump(result,file)
