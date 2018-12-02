methods = { 'authors': authors, 'followers': followers }

def authors(bot, nodes, amount, args) -> List[User]:
    
    authors = []
    
    def _author(media):
            bot.api.media_info(media.id) 
            data = bot.api.last_json["items"][0]["user"]
            id = data["pk"] 
            return User(id=id, data=data)
            
    for node in nodes:
            
            if isinstance(node, Media):
                        authors += [_author(node)] 
                        
            elif isinstance(node, str):
                        media = Media(url=node)
                        authors += author(media)]
            else:
                        raise Exception('cannot get autor from {}'.format(node)
            
    return authors


def followers(bot, nodes, amount, args) -> List[User]:
    
    result = []
    
    def _followers(node) -> List[User]:
            return [User(id=item['pk']) for item in self.api.get_total_followers(node.id, amount)]
    
    for node in nodes:
    
            if isinstance(node, User):    
                        result += _followers(node)
                        
            elif isinstance(node, str):
                        user = User(username=node)
                        result += _followers(user)
            
    return [users for users in result][::-1] if result else []
    


def make_methods(bot):
     return { key: partial(value, bot) for (key, value) in methods.items() }


