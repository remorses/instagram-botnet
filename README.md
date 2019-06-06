# instagram-botnet [![CircleCI](https://circleci.com/gh/remorses/instagram-botnet/tree/master.svg?style=svg)](https://circleci.com/gh/remorses/instagram-botnet/tree/master)
Write readable declarative yaml files to control your botnet
---

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
template_name: test_follow,
action_name: test_follow_famous_people,
type: follow
node: kimkarkdashian
args: {}
metadatat: { 
username:
proxy:
}
```
another example for message
```
type: message
...
args: {
messages: ["ciao"],
}
```

Other events are emitted, for example when someone followes you:
```
type: got_followed,
node: username,
...
```


