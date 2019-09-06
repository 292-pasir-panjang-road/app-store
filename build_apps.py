import sys
from utils import build_apps

if __name__ == "__main__":
    tag = sys.argv[1]
    build_apps(tag)