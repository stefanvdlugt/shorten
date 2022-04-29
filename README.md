# shorten
*a simple URL shortener written in Flask*

- add, edit, and delete tasks
- set deadlines
- receive reminders by mail

## Installation and usage

### Using docker-compose (easiest)
Clone the repository:
```
git clone https://github.com/stefanvdlugt/shorten.git
cd shorten/
```
Rename/copy the file `settings.env.sample` to `settings.env` and edit it to set some application options.
Then run the following commands:
```
docker-compose build
docker-compose up -d
```
The application will listen on port 5000.

### Standalone, using Python
Clone the repository
```
git clone https://github.com/stefanvdlugt/shorten.git
cd shorten/
```
(Optionally) create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
pip install gunicorn
```
Rename/copy the file `settings.env.sample` to `settings.env` and edit it to set some application options.
Then run the application:
```
./run.sh
```

