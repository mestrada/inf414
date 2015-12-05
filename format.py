__author__ = 'Matias Estrada'

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

if r.get('author_last_idx') is None:
    r.set('author_last_idx', 0)

if r.get('article_last_idx') is None:
    r.set('article_last_idx', 0)

def format_entry(name):
    return name.strip().lower()


def set_entry(name, etype):
    try:
        last_idx = int(r.get('{0}_last_idx'.format(etype)))
        r.set('{0}.{1}'.format(etype, name), last_idx + 1)
        r.set('{0}_last_idx'.format(etype), last_idx + 1)
    except Exception:
        r.delete(name)
        raise


def set_index(entry, entry_type):
    formatted_name = format_entry(entry)
    if r.get(formatted_name) is None:
        set_entry(formatted_name, entry_type)
