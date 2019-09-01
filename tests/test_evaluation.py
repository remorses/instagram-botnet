import pytest
from instabotnet.errors import Stop
from instabotnet.execute import obj_from_yaml


def test_spec():
    z = 'xxx'
    data = dict(
        x=[1, 2, 3,],
        z=z
    )
    s = '''
    nodes: {{ list(data.x) }}
    evaluated_text: {{
        "ciaoo " + str(data.x)
    }}
    ciao: {{ update('y', data.z) }}
    '''
    y = obj_from_yaml(s, data)
    print(y)
    assert data['y'] == z

def test_stop():
    s = '''
    {{ stop() if True else None }}
    '''
    with pytest.raises(Stop):
        obj_from_yaml(s, )



