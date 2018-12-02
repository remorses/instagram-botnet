methods = { 'authors': authors }

def authors(bot, nodes, amount, args) -> List[User]:
    
    authors = []
    
    def _author(media):
            bot.api.media_info(media.id) 
            data = bot.api.last_json["items"][0]["user"]
            id = data["pk"] 
            return User(id=id, data=data)
            
    def _author_from_url(url): 
            media = Media(url=url)
            return author(media)
            
    if isinstance(node, Media):
            authors += [_author(node) for node in nodes]
            
    else:
            authors += [_author_from_url(url) for url in nodes]
            
    return authors


def followers(bot, nodes, amount, args) -> List[User]:
    
    result = []
    
    def _followers(node) -> List[User]:
            return [User(id=item['pk']) for item in self.api.get_total_followers(node.id, amount)]
    
    for node in nodes:
    
            if isinstance(node, User):    
                        result += _followers(node)
                        
            else:
                        user = User(name=node)
                        result += _followers(user)
            
    return [user for user in result][::-1] if result else []
    


def make_methods(bot):
     return { key: partial(value, bot) for (key, value) in methods.items() }


