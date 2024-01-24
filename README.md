# Polymath

Polymath is a web server designed to host resource packs of the Oraxen plugin.
__ __
## How to use Polymath

- Clone the project
``git clone git@github.com:oraxen/Polymath`` or ``git clone https://github.com/oraxen/Polymath``
this fork: ``git clone git@github.com:oOHiyoriOo/polymath.git`` or ``git clone https://github.com/oOHiyoriOo/polymath.git``

- Cd in the directory
``cd ./Polymath``

#### With nix package management
- Install nix
Follow this tutorial (you only need nix, not nixos): https://nixos.org/download.html
On linux this is just this command:
``sh <(curl -L https://nixos.org/nix/install) --daemon``
On macos:
``sh <(curl -L https://nixos.org/nix/install)``
You can check the website to get it working on windows or docker.

- Install the required libs
If you installed nix, just type:
``nix-shell``

#### Without nix package management (and Windows)
If you didn't install nix, you need to install Python 3.8 with those packages:
```
cython
aiohttp
toml
```

- Build polymath
```sh
./build.sh
```

- Run a first time
``sh
./run``

- Configure the file ``polymath/config/settings.toml``

- Run a second time
``sh
./run``

- Polymath should now be running

__ __
## How to use on Pterodactyl or Windows

- Clone the project
``git clone git@github.com:oraxen/Polymath`` or ``git clone https://github.com/oraxen/Polymath``

- Install [Python](https://python.org) (tested on 3.10!)

- install following requirements (use pip or requirements.txt):
``pip  install -r requirements.txt``

- run:  `python run`
- 
##### Installing Requirements:
```
aiohttp>=3.7.4
toml>=0.10.2
colorama>=0.4.5
```
#### you **must** setup SSL for this to work! 

### if using nginx:
- setup a new vhost in /etc/nginx/sites-available/
- setup ssl (u can use [certbot](https://certbot.eff.org/))
- change the location of the VHOST to something like: 
```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header X-Real-IP $remote_addr;
    client_max_body_size 10M;
}
```
> i recommend using a subdomain like texture.example.xyz
- make sure port 443 is forwarded!
