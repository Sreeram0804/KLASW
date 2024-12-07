import json

with open('Input/Milestone6b.json','r') as file:
    data=json.load(file)

steps_data=data['steps']
machines_data=data['machines']
wafers_data=data['wafers']

schedule=[]

running={}
finished={}
for machine in machines_data:
    running[machine['machine_id']]=[]

for step in steps_data:
    finished[step['id']]=[]

wafers={}
quantity={}

#To find the wafers to be inserted into the machines(iterates and finds all the wafer_id)
#Also uses quantity to check how many wafers are being processed for each step
#This will be used in the latter part to stop the program when done
for wafer in wafers_data:
    type=wafer['type']
    for wafer_num in range(1,wafer['quantity']+1):
        wafers[type+'-'+str(wafer_num)]=wafer['processing_times']
        for i in wafer['processing_times'].keys():
            if(i not in quantity.keys()):
                quantity[i]=0
            quantity[i]+=1


#To make sure that the wafer is not run again for a step or run when it is in a machine
def check(wafer,finished,running):
    for process_wafers in running.values():
        if(wafer in process_wafers):
            return False
    if(wafer in finished):
        return False
    return True


#To check if the parameters are within the specified range
def check_parameters(step_id,steps,machine,m_parameters):
    for step in steps_data:
        if(step['id']==step_id):
            param=step['parameters']
            for parameter in param.keys():
                if(param[parameter][0]>m_parameters[parameter] or param[parameter][1]<m_parameters[parameter]):
                    return False
    return True  


#To check if all dependencies are satisfied for a specific wafer
def check_dependency(step_id,wafer,finished):
    for step in steps_data:
        if(step['id']==step_id and step['dependency']!=None):
            for depend in step['dependency']:
                if(wafer not in finished[depend]):
                    return False
            break
    return True


#checks if machine is currently unoccupied,if all parameters are satisfied and not in cooldown
def first_check(running,step_id,steps_data,machine_id,parameters,fluctuation_cooldown,time):
    if(running[machine_id]==[] and check_parameters(step_id,steps_data,machine_id,parameters) and fluctuation_cooldown[machine_id]<=time):
        return True
    return False


#checks if wafer has a step to be processed in this machine,is currently running or finished the step and checks dependency
def second_check(step_id,wafer,wafers,finished,running,cuurent_finished):
    if(step_id in wafers[wafer].keys() and wafers[wafer][step_id]!=0 and check(wafer,finished[step_id],running) 
       and wafer not in current_finished and check_dependency(step_id,wafer,finished)):
        return True
    return False


fluctuation_quantity={}#keeps track of n for each machine
fluctuation_cooldown={}#keeps track of cooldown time for each machine(fluct_cooldown_time<=time) where fluct_cooldown_time=time+cooldown_time
machine_parameters={}#keeps a copy of machine parameters, to store changes in the parameters
for machine in machines_data:
    fluctuation_quantity[machine['machine_id']]=machine['n']
    fluctuation_cooldown[machine['machine_id']]=0
    machine_parameters[machine['machine_id']]=machine['initial_parameters'].copy()


time=0
while(True):
    current_finished=[]
    for machine in machines_data:
        #checks if machine is currently unoccupied,if all parameters are satisfied and not in cooldown
        if(first_check(running,machine['step_id'],steps_data,machine['machine_id'],machine_parameters[machine['machine_id']],fluctuation_cooldown,time)):
            for wafer in wafers:
                #checks if wafer has a step to be processed in this machine,is currently running or finished the step and checks dependency
                if(second_check(machine['step_id'],wafer,wafers,finished,running,current_finished)):

                    #running stores {machine_id:[wafer_id,end_time]}
                    running[machine['machine_id']]=[wafer,time+wafers[wafer][machine['step_id']]]
                    schedule.append({'wafer_id':wafer,'step':machine['step_id'],'machine':machine['machine_id'],'start_time':time,'end_time':time+wafers[wafer][machine['step_id']]})
                    break
        else:
            if(fluctuation_cooldown[machine['machine_id']]<=time and running[machine['machine_id']][1]-1==time):
                finished[machine['step_id']].append(running[machine['machine_id']][0])
                current_finished.append(running[machine['machine_id']][0])

                #Removing wafers which are processed completely
                name=running[machine['machine_id']][0]
                for waf in wafers_data:
                    if(waf['type']==name.split('-')[0]):
                        f=0
                        for i in waf['processing_times'].keys():
                            if(name not in finished[i]):
                                f=1
                                break
                        if(f==0):
                            wafers.pop(name)
                        break

                running[machine['machine_id']]=[]
                fluctuation_quantity[machine['machine_id']]-=1
                
                #fluctuation to the machines parameters are added
                if(fluctuation_quantity[machine['machine_id']]==0):
                    fluctuation_quantity[machine['machine_id']]=machine['n']
                    temp_param=machine_parameters[machine['machine_id']]
                    for key in temp_param.keys():
                        if(key in machine['fluctuation'].keys()):
                            temp_param[key]=temp_param[key]+machine['fluctuation'][key]
            
            #checks if the machines parameters are in range else puts it in cooldown
            if(check_parameters(machine['step_id'],steps_data,machine['machine_id'],machine_parameters[machine['machine_id']])==False):
                fluctuation_cooldown[machine['machine_id']]=time+machine['cooldown_time']+1
                machine_parameters[machine['machine_id']]=machine['initial_parameters'].copy()
    time+=1
    flag=1

    #to check if all the wafers and their steps have been completed
    for step in steps_data:
        if(len(finished[step['id']])!=quantity[step['id']]):
            flag=0
            break
    if(flag==1):
        break

print(schedule)

result={'schedule':schedule}
with open('MilestoneOptimize.json','w') as file:
    json.dump(result,file)
