
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

jobs = [make_job(group, bots) for group in script['execute']]

threads = [Executer(job) for job in jobs]

start(threads)

wait(threads)


def prepare(script) -> bots:
 pass


class Job:
        def __init__(self, state, actions):
                self.state = state
                self.actions = actions

def make_job(group, bots) -> Job:
        
        def make_action(obj): 
                return { 'method': edge, 'amount': amount  for edge, amount in obj.items()[0]}  

        interaction, body = group.items()[0]
        
        if 'from_nodes' in body:
                state = { 'target_nodes': body['from_nodes'], bots: bots }
                actions = [ make_action(edge) for edge in body['via_edges'] ]
                actions += [{ 'method': interaction, 'amount': 1 }]
        elif 'nodes' in body:
                state = { 'target_nodes': body['nodes'], bots: bots }
                actions =  [{ 'method': interaction, 'amount': 1 }]
        else:
                raise Exception
                
        return Job(state, actions) 
        
def identity(*args, **kwargs):
        raise Exception

def reducer(state, action):
    nodes = state['target_nodes']
    bots = state['bots']
    next_nodes = []
    
    if state['exception']:
        send_bot_to_phone_verifier
        change_bot_if_neccessary
        resolve_captcha_if_necessary
        sleep_more
        remove_bot_if_broken
    
    for id, bot in enumerate(bots):
    
        bot_nodes = [node for i, node in enumerate(nodes) if i % len(bots) == id]
        
        method = methods.get(action['method'], identity)
        
        next_nodes += method(bot, bot_nodes, action['amount'], action['args'])
        
     return { 'target_nodes': next_nodes, 'bots': bots }


def start(threads): 
        [thread.start() for thread in threads]
        
def wait(threads):
        [thread.join() for thread in threads]


class Executer(Thread):
    def __init__(self, job):
        self.actions = job.actions
        self.state = job.state
    
    def start(self):
        reduce(reducer, self.state, self.actions)



