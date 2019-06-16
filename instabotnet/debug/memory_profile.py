

def memory_summary():
    # Only import Pympler when we need it. We don't want it to
    # affect our process if we never call memory_summary.
    from pympler import summary, muppy
    mem_summary = summary.summarize(muppy.get_objects())
    rows = summary.format_(mem_summary)
    return '\n'.join(rows)
