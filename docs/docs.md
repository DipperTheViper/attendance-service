### Docs
use PlantUML (if you have error, run this):
```shell
sudo apt install graphviz
```


___

### CONVENTIONS

- backend port is `8966`

___
#### Domains:

- api: https://mpm13-api.fazelidev.ir

___




#### object storage
```nginx
location /media {
        proxy_pass http://mpm13-object-storage-nginx/media;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_cache_bypass $http_upgrade;
        proxy_pass_request_headers on;
   }
```
