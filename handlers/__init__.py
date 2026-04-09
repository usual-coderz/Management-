from .start import register_handlers
from .group_commands import register_group_commands
#from .repo import register_repo_handler
from .forcejoin import register_forcejoin


def register_all_handlers(app):
    register_handlers(app)
    #register_repo_handler(app)
    register_group_commands(app)
    register_forcejoin(app)

    print("✅ All handlers registered!")