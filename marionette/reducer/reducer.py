
methods = {
    'like': like,
    'followers': followers
    }

def like(bot, nodes, args):
    for media in nodes:
        if bot.api.like(media):
            return bot.api.last_json['likes']
        else:
         raise Error

def reducer(state, action):
    nodes = state['nodes']
    bot = state['bot']
    
    if state['exception']:
        handleit
        change_bot_if_neccessary
        resolve_captcha_if_necessary
        sleep_more
        
    try:
        next_nodes = methods.get(action['method'], identity)(bot, nodes, action['amount'], action['args'])
        
    catch ex:
        return {...state, 'exception': ex}
        
    # keep track of shared data among bots,
    # like all the followers of a given user can be collected among bots searching
    # the edge method with a particular from node.
    state['done'][action['method']] = {'from': nodes, 'to':next_nodes}
    
    return {'nodes': next_nodes, 'bot': bot}  

# the block of actions below is partitoned around some bots and then executed by a thread per bot
# but first from the yaml object is derived some actions and the initial state for the reducer function,
# executed in the thread
"""
- follow:
        from_nodes: [user1, user2]
        via_edges: 
                - followers: 10
"""
# the yaml above is then parsed in these 2 actions
actions = [{'method': 'followers', 'amount': 10}, {'method': 'follow', 'amount': 1},]
# the initial state is set eith the users in from_nodes
state = {'nodes': from_nodes, 'bot': Bot(u, p)}

# every gorup of actions is partitioned around some bots, every bot or bot group
# execute their partition in a separate thread and then main thread wait for them.
# if the main action is an export then at the end of the thread execution data is stored 
# in some file or class
class Executer(Thread):
    def __init__(self, state, actions):
        self.actions = actions
    
    def start(self):
        reduce(reducer, state, actions)
        
"""

script is made of Jobs
A Job is a group of actions
an action is a search of new nodes from relations to others (edge)
or an interaction against nodes thatin relation to others (interaction)

"""

def partitionate_actions(script, bots):
        states =  map(make_state, script['execute'])
        actions = map(make_actions, script['execute'])
        return zip(states, actions)

map(
# start all the bots with their partition of work
action_groups = partitionate_actions(script, bots)

def run_actions(actions, bot) -> Thread:
        executer = Executer(actions, bot)
        executer.start()
        return executer


threads = action_group.map(lambda actions, bot: run_actions(actions, bot))

# wait for all bots, everyone in his own thread
wait(threads)


        

# TODO: how to share data between executers?
# how to make unison mode?
# how to export data in sync for every action?