with import <nixpkgs> { };

let
  polymath = python38.withPackages (python-packages:
    with python-packages; [
      cython
      aiohttp
      toml
    ]);
in stdenv.mkDerivation {
  name = "polymath-dev-environment";
  buildInputs = [ polymath ];
}