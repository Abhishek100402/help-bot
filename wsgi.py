# wsgi.py
from importlib import import_module

# try to load either create_app() (factory) or app (instance)
mod = import_module("app")

if hasattr(mod, "create_app"):
    app = mod.create_app()
elif hasattr(mod, "app"):
    app = mod.app
else:
    raise RuntimeError(
        "app module must provide either create_app() or app instance (top-level)."
    )
