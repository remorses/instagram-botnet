
import fastjsonschema
import yaml
import collections
import os.path



def load(path):
    current = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current, path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f.read())

geotag_schema = load('geotag.yaml')
user_schema = load('user.yaml')
media_schema = load('media.yaml')
comment_schema = load('comment.yaml')
story_schema = load('story.yaml')


store = dict(
        geotag_schema=geotag_schema,
        user_schema=user_schema,
        media_schema=media_schema,
        comment_schema=comment_schema,
        story_schema=story_schema,
)


def resolve_refs(spec, uri='', store={}):

    resolver = fastjsonschema.RefResolver(uri, spec, store=store)

    def _do_resolve(node):
        if isinstance(node, collections.abc.Mapping) and '$ref' in node:
            with resolver.resolving(node['$ref']) as resolved:
                return resolved
        elif isinstance(node, collections.abc.Mapping):
            for k, v in node.items():
                node[k] = _do_resolve(v)
        elif isinstance(node, (list, tuple)):
            for i in range(len(node)):
                node[i] = _do_resolve(node[i])
        return node

    return _do_resolve(spec)

geotag_schema = resolve_refs(geotag_schema, store=store)

user_schema = resolve_refs(user_schema, store=store)

media_schema = resolve_refs(media_schema, store=store)

comment_schema = resolve_refs(comment_schema, store=store)

story_schema = resolve_refs(story_schema, store=store)
