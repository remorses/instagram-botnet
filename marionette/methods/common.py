from functools import wraps


def accepts(Class):

    def _accepts(original):

        @wraps(original)
        def enhanced(bot, nodes, amount, args, *others, **kwrgs):

            print('nodes in accepts for {}: {}'.format(original.__name__, nodes))

            if any([not isinstance(node, Class) for node in nodes]):
                raise Exception(
                    'nodes like {} aren\'t instance of {}'.format(nodes[0], Class.__name__))

            result = original(bot, nodes, amount, args, *others, **kwrgs)

            return result

        enhanced.accepts = Class

        return enhanced

    return _accepts
