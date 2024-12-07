import json

with open('Input/Milestone2b.json','r') as file:
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
    flag=1
    for step in steps_data:
        if(len(finished[step['id']])!=quantity):
            flag=0
            break
    if(flag==1):
        break

print(schedule)

result={'schedule':schedule}
with open('Milestone2bOutput.json','w') as file:
    json.dump(result,file)