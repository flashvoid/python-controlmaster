# pycm

Simple wrapper around ssh implementing put, get, exe via [ControlMaster](https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing) multiplexing.

Generaly used for same tasks as [paramiko](https://github.com/paramiko/paramiko) or [fabric](https://github.com/fabric/fabric)
but act as real user and so better handle complex [ssh_config](https://linux.die.net/man/5/ssh_config) files
with long redirect chains especially

## Usage

```console
> git clone git://github.com/flashvoid/python-controlmaster.git pycm
```

```python
from pycm import ControlMaster

ssh = ControlMaster("customhost")
ssh.connect()
ssh.put(src,dst)
ssh.exe(cmd)
ssh.get(src,dst)
ssh.disconnect()
```

## TODO

- [ ] Think of a way to suppress all this trash on stdout
