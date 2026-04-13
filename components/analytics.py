
def global_stats(data):
    max_pop = max(data, key=lambda x: x.get("population") or 0)
    max_area = max(data, key=lambda x: x.get("area") or 0)
    return max_pop, max_area
