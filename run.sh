#!/bin/bash
if [ -f venv/bin/activate ]; then
	echo Activating virtualenv...
	source venv/bin/activate
fi
echo Upgrading database...
flask db upgrade
echo Launching application...
gunicorn -b :5000 --access-logfile - --error-logfile - run.py:app

