
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



actions = [{'method': 'like', 'amount': 10},]



class Executer(Thread):
    def __init__(self, actions):
        self.actions = actions
    
    def start(self):
        self.actions.reduce(reducer, 
        {nodes: from_nodes, bots: [Bot(u, p)]})


action_groups = partitionate_actions(script)


# start all the bots with their partition of work
threads = []
for actions in action_group:
        executer = Executer(actions)
        threads += [executer]
        executer.start()

# wait for all bots, everyone in his own thread
for t in threads:
        t.join()
        

# TODO: how to share data between executers?
# how to make unison mode?
# how to export data in sync for every action?