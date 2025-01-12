# Deploy
`nginx must be installed on the host`

First create a virtual environment and install prerequisites:
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install gunicorn
```
Next edit the /etc/nginx/nginx.conf adding these lines at the bottom of the `http` config block:
```server {
                listen 80;
                server_name sscsurvey.ru;
                access_log /var/log/nginx/sscsurvey.log;

                location / {
                        proxy_pass http://127.0.0.1:8000;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                }
        }

        server {
                listen 8080;
                server_name sscsurvey.ru;
                access_log /var/log/nginx/sscsurvey.log;

                location / {
                        proxy_pass http://127.0.0.1:8000;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                }
        }
```
Now restart the nginx and run the WSGI server with:
```
nginx -s reload
.venv/bin/gunicorn -w 8 sscs:app &
```
