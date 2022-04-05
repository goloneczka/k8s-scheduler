class Node:

    def __init__(self, custom_obj):
        self.name = custom_obj['metadata']['name']
        self.cpu_usage = custom_obj['usage']['cpu']
        self.memory_usage = custom_obj['usage']['memory']
