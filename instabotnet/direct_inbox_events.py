from funcy import ignore
from .bot import Bot
from datetime import datetime


def direct_inbox_events(bot: Bot):
    try:
        data = bot.api.direct_v2_inbox()
        my_pk = str(data['viewer']['pk'])
        unseen_count = data['inbox']['unseen_count']
        if unseen_count > 0:
            for thread in data['inbox']['threads']:
                last_seen_at = int(thread['last_seen_at'][my_pk]['timestamp'])
                thread_id = thread['thread_id']
                if int(thread['last_activity_at']) > last_seen_at:
                    res = bot.api.direct_v2_thread(thread_id)
                    for item in res['thread']['items']:
                        if str(item['user_id']) != my_pk and int(item['timestamp']) > last_seen_at:
                            item_type = item['item_type']
                            item_id = item['item_id']
                            if item_type == 'text':
                                bot.api.mark_item_as_seen(thread_id, item_id)
                                pk = str(item['user_id'])
                                users = [user for user in thread['users'] if pk == str(user['pk'])]
                                username = users[0]['username'] if len(users) else ''
                                yield ({
                                    'type': 'message',
                                    # 'metadata': bot.metadata, TODO
                                    'args': {
                                        'message': item['text'],
                                        'thread_id': thread_id,
                                        'item_id': item_id,
                                    },
                                    'node': {
                                        'type': 'user',
                                        'pk': pk,
                                        'username': username,
                                    },
                                    'timestamp': int(item['timestamp'])
                                })
                            else: # TODO
                                bot.logger.warning(f'skipping message of type {item_type} as not implemented')
    except Exception as e:
        print(e)
        return []

