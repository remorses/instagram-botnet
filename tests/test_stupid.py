from .support import *




@pytest.mark.asyncio
async def test_only_evaluation():
    template = """
    {{ print('heeey')}}
    {{None}}
    """
    data = {
        **env,
    }
    result = await async_execute(template, data)
    # print(json.dumps(data['settings'], indent=4))
    print(json.dumps(result, indent=4))


@pytest.mark.asyncio
async def test_exiting():
    template = """
    {{ print('sto per uscire bro')}}
    ---
    {{exit()}}
    """
    data = {
        **env,
    }
    with pytest.raises(SystemExit):
        result = await async_execute(template, data)
        # print(json.dumps(data['settings'], indent=4))
        print(json.dumps(result, indent=4))

