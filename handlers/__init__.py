from .start import register_handlers
from .group_commands import register_group_commands
from .repo import register_repo_handler

# 👉 Import forcejoin so decorators register ho jaye
from . import forcejoin


def register_all_handlers(app):
    register_handlers(app)
    register_repo_handler(app)
    register_group_commands(app)

    print("✅ All handlers registered (including Force Join)!")