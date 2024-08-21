# pycm

Simple wrapper around ssh implement put, get, exe via controlmaster session.

Generaly used for same tasks as paramiko or fabric
but act as real user and so better handle complex ssh_config files
with long redirect chains especially

## Usage

```console
> git clone git://github.com/flashvoid/python-controlmaster.git pycm
```

```python
from pycm import controlmaster

customer = controlmaster.controlmaster('customhost')
customer.connect()
customer.put(src,dst)
customer.exe(cmd)
customer.get(src,dst)
customer.disconnect()
```

## TODO

- [ ] Think of a way to suppress all this trash on stdout
