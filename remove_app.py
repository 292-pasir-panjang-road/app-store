from utils import remove_app
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--subdomain',   type=str,  dest='sub_domain', required=True, help='The sub domain of the app')
  args = parser.parse_args()
  result = remove_app(args.sub_domain)
  print(result)