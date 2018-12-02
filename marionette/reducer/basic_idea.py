
"""
1. divide the script in 2 parts:
 - prepare
 - execute
 the prepare part initialize the bots and set some global variables
 the execute part execute search and interaction to nodes and thei relations
2. divide the execute object in an array of Jobs
 every job is an object like { state: State, actions: [Action] }
 state is the description of the current bot session.
 State is like { bot: Bot, target_nodes: [Node] }
 actions are the actions executed by the bot starting from the initial nodes 
 and updating the state with the next ones.
 an action is an object like { method: Edge | Interaction, amount: number }
3. execute every Job distributing work equally among bots, 
 according to the script mode, bots will execute the final interaction for a partition of the 
 final target nodes (if mode == distributed) or every bot to all the final nodes (if mode == unison)
"""

bots = make_bots(script)

for data in script['execute']:

    task = make_task(data)

    jobs = [make_job(part, bot) for (part, bot) in partitionate(task, bots)]
    
    threads = [Executer(job) for job in jobs]
    
    threads = start(threads)

    threads = wait(threads)
    
    
    
    
    
    
    
    
    
    
    
    
    
    

bots = make_bots(script)

for data in script['execute']:

    task = make_task(data)
    threads = []
    
    for (task, bot) in partitionate(task, bots):
        state = make_state(task, bot)
        actions = make_actions(task)
        threads += [Reducer(state, actions)]

    threads = start(threads)
    threads = wait(threads)
    threads = reset(threads)
    
    
    
    
    
    
    
    




def make_bots(script):

    bots = []

    for i, credentials in enumerate(script['bots']):
        bots += [Bot(**credentials)]

    for bot in bots:
        if 'max_per_day' in script:
            bot.max_per_day = {
                key: value for key, value in script['max_per_day']}
        if 'delay' in script:
            bot.delay = {key: value for key,
                         value in script['delay']}

    return bots



def make_task(data):
        
        nodes = []
        actions = []
        args = {}
        
        interaction, body = data.items()[0]
        
        if 'nodes' in body:
                nodes += body['nodes']
                args = body['args']
                actions += [dict(type=interaction, amount=1)]
                
        elif 'from_nodes' in body:
                nodes += body['from_nodes']
                args = body['args']
                edges = body['via_edges']
                actions += [dict(type=edge, amount=num, args=[]) for (edge, num) in edges)]
                actions += [dict(type=interaction, amount=1, args=args)]
        else:
                raise Exception
                
        return Task(nodes=nodes, actions=actions)
                
                


def prepare(script) -> bots:
   pass



def partitionate(task: Task, bots):
        
        couples = []

        for partition, bot in enumerate(bots):
        
            _right_partition = lamda i: (i % len(bots)) == partition
            new_nodes = [node for (i, node) in enumerate(task.nodes) if _right_partition(i)]
            new_task = Task(nodes=new_nodes, amount=task.amount, args=task.args)
            result += [(new_task, bot)]
            
        return couples   

class Task(dict):
    """"
    task:
        
        nodes: [node1, node2]
        

        
        actions: 
        
                - type:   feed
                  amount: 10
                  
                - type:   send
                  amount: 1
                  args: 
                    messages = []
                    stuff =    whokonws
    """
    pass


class Job:
        def __init__(self, state, actions):
                self.state = state
                self.actions = actions
            

def make_job(task: Task, bot) -> Job:

        state   = make_state(task, bot)
        actions = make_actions(task)
                
        return Job(state, actions) 
        

def make_state(task, bot):
        state = State(target_nodes=task.nodes, bot=bot, errors=[])
        return state


def _make_action(action) -> Action: 
        args = action.args if action.args else {}
        return Action(type=action.type, amount=action.amount, args=args)

def make_actions(task):            
        actions += [ _make_action(action) for action in task.actions]
        


def reducer(state: State, action: Action):
    nodes = state.target_nodes
    bots = state.bots
    errors = state.errors
    
    if errors:
        send_bot_to_phone_verifier
        change_bot_if_neccessary
        resolve_captcha_if_necessary
        sleep_more
        remove_bot_if_broken
        
    try:
        method = methods.get(action.type, raiser)
        next_nodes = method(bot, nodes, action.amount, action.args)
        
    catch Exception as ex:
        return State(target_nodes = nodes, bot = bot, errors = (errors += [ex])) 
        
    return  State(target_nodes = next_nodes, bot = bot, errors = errors)
    


class State(dict):
    pass

class Action(dict):
    pass



def start(threads): 
        [thread.start() for thread in threads]
        return threads
        
def wait(threads):
        [thread.join() for thread in threads]
        return threads

def reset(threads):
        return []





class Executer(Thread):

    def __init__(self, job):
        self.actions = job.actions
        self.state = job.state
    
    def run(self):
        reduce(reducer, self.state, self.actions)
        



class Reducer(Thread):

    def __init__(self, state, actions):
        self.actions = actions
        self.state = state
    
    def run(self):
        reduce(reducer, self.state, self.actions)
        
        






