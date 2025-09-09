#!/usr/bin/env python3
import os
from app import create_app


if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app = create_app()
    app.run(host=host, port=port, debug=debug)