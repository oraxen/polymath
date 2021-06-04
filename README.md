# Polymath

Polymath is a web server designed to host resource packs of the Oraxen plugin.

## How to use Polymath

- Clone the project
``git clone git@github.com:oraxen/Polymath`` or ``git clone https://github.com/oraxen/Polymath``

- Cd in the directory
``cd ./Polymath``

- Install the required libs
On nixos: ``nix-shell``

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
