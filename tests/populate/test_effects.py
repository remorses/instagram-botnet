from instabotnet.populate import populate_string


interact_with_partition = """
{{ stop() if len(set(partition) - set(interacted)) == 0 else None }}
---
name: {{ campaignName + ' intearacting people' }}

actions:
    -
        name: 1
        nodes: {{ 
            list(set(partition) - set(interacted))
        }}
        from: user
        edges:
            - follow
            - scrape:
                key: new_interacted
                model: x.username
            - feed:
                amount: 5
            - like
---
{{ data.update({'interacted': interacted + new_interacted}) }}
"""

def test_1():
    populate_string(interact_with_partition, {
        'partition': [['asd']],
        'interacted': [],
        'new_interacted': [['asd']],
    })
