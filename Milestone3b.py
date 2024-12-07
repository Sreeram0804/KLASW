import json

with open('Input/Milestone3b.json','r') as file:
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
quantity={}
for wafer in wafers_data:
    type=wafer['type']
    for wafer_num in range(1,wafer['quantity']+1):
        wafers[type+'-'+str(wafer_num)]=wafer['processing_times']
        for i in wafer['processing_times'].keys():
            if(i not in quantity.keys()):
                quantity[i]=0
            quantity[i]+=1

def check(wafer,finished,running):
    for process_wafers in running.values():
        if(wafer in process_wafers):
            return False
    if(wafer in finished):
        return False
    return True

def check_parameters(step_id,steps,machine,m_parameters):
    for step in steps_data:
        if(step['id']==step_id):
            param=step['parameters']
            for parameter in param.keys():
                if(param[parameter][0]>m_parameters[parameter] or param[parameter][1]<m_parameters[parameter]):
                    return False
    return True  

fluctuation_quantity={}
fluctuation_cooldown={}
machine_parameters={}
for machine in machines_data:
    fluctuation_quantity[machine['machine_id']]=machine['n']
    fluctuation_cooldown[machine['machine_id']]=0
    machine_parameters[machine['machine_id']]=machine['initial_parameters'].copy()

# quantity=len(wafers)
time=0
while(True):
    for machine in machines_data:
        if(running[machine['machine_id']]==[] and check_parameters(machine['step_id'],steps_data,machine['machine_id'],machine_parameters[machine['machine_id']]) and fluctuation_cooldown[machine['machine_id']]<=time):
            for wafer in wafers:
                if(machine['step_id'] in wafers[wafer].keys() and wafers[wafer][machine['step_id']]!=0 and check(wafer,finished[machine['step_id']],running)):
                    name=wafer
                    running[machine['machine_id']]=[name,time+wafers[wafer][machine['step_id']]]
                    schedule.append({'wafer_id':name,'step':machine['step_id'],'machine':machine['machine_id'],'start_time':time,'end_time':time+wafers[wafer][machine['step_id']]})
                    break
        else:
            if(fluctuation_cooldown[machine['machine_id']]<=time and running[machine['machine_id']][1]-1==time):
                finished[machine['step_id']].append(running[machine['machine_id']][0])
                running[machine['machine_id']]=[]
                fluctuation_quantity[machine['machine_id']]-=1
                if(fluctuation_quantity[machine['machine_id']]==0):
                    fluctuation_quantity[machine['machine_id']]=machine['n']
                    #to add fluctuation
                    temp_param=machine_parameters[machine['machine_id']]
                    for key in temp_param.keys():
                        if(key in machine['fluctuation'].keys()):
                            temp_param[key]=temp_param[key]+machine['fluctuation'][key]
                    # for param in machine_parameters[machine['machine_id']].keys():
                    #     machine_parameters[machine['machine_id']]+=machine['fluctuation']
                    machine_parameters[machine['machine_id']]=temp_param
            if(check_parameters(machine['step_id'],steps_data,machine['machine_id'],machine_parameters[machine['machine_id']])==False):
                fluctuation_cooldown[machine['machine_id']]=time+machine['cooldown_time']+1
                machine_parameters[machine['machine_id']]=machine['initial_parameters'].copy()
    time+=1
    flag=1
    for step in steps_data:
        if(len(finished[step['id']])!=quantity[step['id']]):
            flag=0
            break
    if(flag==1):
        break

print(schedule)

result={'schedule':schedule}
with open('Milestone3bOutput.json','w') as file:
    json.dump(result,file)