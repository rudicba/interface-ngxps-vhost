from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class NgxpsVhostRequires(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:ngxps-vhost}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{requires:ngxps-vhost}-relation-{departed,broken}')
    def broken(self):
        self.remove_state('{relation_name}.available')

    # Send relation data when site is ready
    def configure(self, listen='80', root='', RewriteLevel='CoreFilters',
                  EnableFilters='', LearningMode=False):
        self.set_remote(
            listen=listen,
            root=root,
            RewriteLevel=RewriteLevel,
            EnableFilters=EnableFilters,
            LearningMode=LearningMode
        )
