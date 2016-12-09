from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class NgxpsVhostProvides(RelationBase):
    scope = scopes.UNIT

    def to_bool(self, value):
        return value.lower() in ['true', 'y', 'yes']

    def to_list(self, value):
        if not value:
            return []

        return [x.strip() for x in value.split(',')]

    def ready(self):
        conv = self.conversation()

        ensure = ['listen', 'root', 'RewriteLevel', 'LearningMode']

        for value in ensure:
            if conv.get_remote(value) is None:
                return False

        return True

    # Use some template magic to declare our relation(s)
    @hook('{provides:ngxps-vhost}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

        if self.ready():
            conv.set_state('{relation_name}.available')
        else:
            conv.remove_state('{relation_name}.available')

    @hook('{provides:ngxps-vhost}-relation-{broken,departed}')
    def broken(self):
        # Remove the state that our relationship is now available
        # to our principal layer(s)
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.available')

    def contexts(self):
        contexts = []
        for conv in self.conversations():
            context = {
                'service_name': conv.scope.split('/')[0],
                'listen': conv.get_remote('listen'),
                'server_name': conv.get_remote('server_name'),
                'root': conv.get_remote('root'),
                'access_log': self.to_bool(
                    conv.get_remote('access_log')
                ),
                'RewriteLevel': conv.get_remote('RewriteLevel'),
                'EnableFilters': self.to_list(
                    conv.get_remote('EnableFilters')
                ),
                'LearningMode': self.to_bool(
                    conv.get_remote('LearningMode')
                ),
            }
            contexts.append(context)

        return contexts
