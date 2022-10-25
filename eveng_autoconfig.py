import json
import sys

from eveng_autoconfig import Autoconfig

def main(argv):
    autoconfig = Autoconfig(json.load(open(argv[1])))
    autoconfig.configure()
    
if __name__ == "__main__":
    main(sys.argv)

