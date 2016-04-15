#!/usr/bin/env python3

from flask import Flask
from myaccount import view,app,register_blueprints


register_blueprints(app)

if __name__ == '__main__':
	app.run(debug=True)
