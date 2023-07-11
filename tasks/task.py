import random, math

class Task:
    def __init__(self, data, output_file:str=None):
        self.data = data
        self.output_file = output_file
    
    def run(self, app_id:str, tenant_id:str, app_secret:str):
        output = sorted(self.data)
        with open(self.output_file, 'w') as f:
            f.write(output)

def create_tasks(params:dict={}): 
    num_tasks = 10
    arr = [random.randint(1, 1000) for i in range(100)]
    part_size = int(math.ceil(len(arr)/num_tasks))
    
    all_tasks = []
    
    for i in range(num_tasks):        
        sub_arr = arr[(i*part_size):min(len(arr), (i+1)*part_size)]
        new_task = Task(sub_arr, f"output-{i}.txt")
        all_tasks += [new_task]
    
    return all_tasks