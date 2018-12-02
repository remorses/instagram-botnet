
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

bots = prepare(script)

for task in script['execute']:

    jobs = [make_job(task, bots, i ) for (i, _) in enumerate(bots)]

    threads = [Executer(job) for job in jobs]

    start(threads)

    wait(threads)


def prepare(script) -> bots:
 pass


class Job:
        def __init__(self, state, actions):
                self.state = state
                self.actions = actions

def make_job(task, bots, partition) -> Job:
        
        def make_action(object) -> Action: 
            edge, amount = object.items()[0]
            return Action(method=edge, amount=amount, args=[])

        interaction, body = task.items()[0]
        
        actions = []
        state = State()
        
        
        if 'from_nodes' in body:
        
                right_partition = lamda i: (i % len(bots)) == partition
                target_nodes = [node for (i, node) in enumerate(body['from_nodes']) if right_partition(i)]
                
                state = State(target_nodes=target_nodes, bot=bots[partition], errors=[])
                
                actions += [ make_action(object) for object in body['via_edges'] ]
                actions += [Action(method=interaction, amount=1, args=body['args'] }]
                
        elif 'nodes' in body:
        
                state = State(target_nodes=body['nodes'], bot=bots[partition], errors=[])
                
                actions += [Action(method=interaction, amount=1, args=body['args'])]
                
        else:
                raise Exception
                
        return Job(state, actions) 


        
def raiser(*args, **kwargs):
        raise Exception

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
        method = methods.get(action.method, raiser)
        next_nodes = method(bot, nodes, action.amount, action.args)
        
    catch Exception as ex:
        return State(target_nodes = nodes, bot = bot, errors = errors += [ex]) 
        
    return  State(target_nodes = next_nodes, bot = bot, errors = errors)
    


class State(dict):
    pass

class Action(dict):
    pass



def start(threads): 
        [thread.start() for thread in threads]
        
def wait(threads):
        [thread.join() for thread in threads]





class Executer(Thread):
    def __init__(self, job):
        self.actions = job.actions
        self.state = job.state
    
    def run(self):
        reduce(reducer, self.state, self.actions)
        
        
        

def make_jobs(script, bots):
        
        for id, bot in enumerate(bots):
                bot_nodes = [node for (i, node) in enumerate(nodes) if i % len(bots) == id]




