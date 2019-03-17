# instagram-bot [![CircleCI](https://circleci.com/gh/remorses/instagram-botnet/tree/master.svg?style=svg)](https://circleci.com/gh/remorses/instagram-botnet/tree/master)
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

with open('test_comment.yaml') as file:
    template = yaml.loads(file.read())
   
execute(template)
```


