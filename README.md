# instagram-botnet [![Build Status](http://fuckclubs.club/api/badges/remorses/instagram-botnet/status.svg)](http://fuckclubs.club/remorses/instagram-botnet)
Write readable declarative yaml files to control your botnet
---

## TODO

- ~~emit events for every action~~
- ~~emit events for new followers, new comments, comment references, usertag references in notifications at login time~~
- ~~rewrite tests using pytest~~
- ~~use drone for ci~~
- emit event at login, adding info like followers nuber, posts number, following, timestamp (so i can later analyse using time window consisting of begin and end sessions)
- emit event at task end
- fix filter, filter should request a model data if given data is not sufficient



## Shell usage

The main module works on yaml script like these:
```yaml

name:                     test_comment

bots:
    -
        username:         username
        password:         password

actions:
    -
        name: comment on 10 posts from @kimkardashian
        nodes:
            - kimkardashian
        edges:
            - user_feed:
                amount: 10
            - comment:
                max:      1
                comments:
                    - ["hello {author}!!!"]
                    - ["come stai?", "come va?"]
                    - ["url works too! http://instagram.com"]

```

To execute the above `test_comment.yaml` run:
```
python3 -m instabotnet test_comment.yaml
```

## Python API usage

To use inside python modules:
```python
from instabotnet import execute

execute('test_comment.yaml', {'username': 'user', 'some_variables': 'bo'})
```


Environment variables are accessible under the env object


The variables passed to execute can be mutated, the execute function returns an object that contains the data collected from he `scrape` action.
The variables are mutated to support the multi script feature, where many templates are chained one after another in a single file and can pass data to the next template mutating the variables.
It is also useful to mutate the settings variable to update the cookies and other data for the next bot iteration.


All the code inside {{ }} is evaluated by an eval call, this means that the templates can be filled with conditional and complex behaviors, for example making an http call to get the caption for uploading a photo, or get a random item from an array variable.
Inside eval code it is avaliable 
- variables
- random module
- all the funcy functions
- variables inside the data object
- urlopen module for making api calls
- json module
A limitation of the code inside {{ }} is that it must consist only of one statement and can only return lists or strings.



Every action inside a template will emit an event, all these events are avaliable in the object returned by execute:
```json
"template_name": "test_follow",
"action_name": "test_follow_famous_people",
"type": "follow",
"node": "kimkarkdashian",
"args": {},
"metadata": { 
    "username": "",
    "proxy": ""
}
```

Other events are emitted, for example when someone followes you:
```
"type": "got_followed",
"node": "username"
```





