class Pod:
    
    def __init__(self, watcher):
        self.namespace = watcher.metadata.namespace
        self.name = watcher.metadata.name
        self.cpu_limit = watcher.spec.containers[0].resources.limits['cpu']
        self.memory_limit = watcher.spec.containers[0].resources.limits['memory']
        self.storage = watcher.spec.ephemeral_containers