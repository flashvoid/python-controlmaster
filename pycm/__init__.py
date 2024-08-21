import sys

from pycm.control_master import ControlMaster

__all__ = [
    "ControlMaster",
]

if __name__ == "__main__":
    assert len(sys.argv) > 1
    host = sys.argv[1]
    if len(sys.argv) > 2:
        debug = sys.argv[2] in ["True", "true", "1"]
    else:
        debug = False
    ssh = ControlMaster(host, debug=debug)
    ssh.connect()
    ssh.exe("uptime")
    ssh.disconnect()
