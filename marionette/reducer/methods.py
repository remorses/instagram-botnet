methods = { 'author': author }

def author(bot, nodes, amount, args):
    
    authors = []
    
    def author_from_id(id):
            bot.api.media_info(id) 
            user_id = bot.api.last_json["items"][0]["user"]["pk"] 
            return User(id = user_id)
            
    def author_from_url(url): 
            user_id = Media.id_from_url(url)
            return author_from_id(user_id)
            
    if isinstance(node, Media):
            authors += [author_from_id(node.id) for node in nodes]
            
    else:
            authors += [author_from_url(url) for url in nodes]
            
    return authors




def make_methods(bot):
     return { key: partial(value, bot) for (key, value) in methods.items() }


