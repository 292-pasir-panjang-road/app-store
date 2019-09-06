import sys
from utils import deploy_apps

if __name__ == "__main__":
  tag = sys.argv[1]
  print(sys.argv)
  deploy_apps(tag)