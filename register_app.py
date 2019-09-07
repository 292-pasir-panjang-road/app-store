from utils import register_app
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--name',        type=str,  dest='name', required=True, help='The name of the app')
  parser.add_argument('--subdomain',   type=str,  dest='sub_domain', required=True, help='The sub domain of the app')
  parser.add_argument('--author',      type=str,  dest='author', required=True, help='The author of the app')
  parser.add_argument('--host',        type=str,  dest='host', default='localhost', help='The host of the app')
  parser.add_argument('--deploy',      type=bool, dest='deploy', default=False, help='whether to deploy the app')
  parser.add_argument('--description', type=str,  dest='description', default="description", help='The description of the app')
  parser.add_argument('--framework',   type=str,  dest='framework', default='flask', help='The framework of the app')
  parser.add_argument('--memory',      type=int,  dest='memory', default=128, help='The memory of the app')
  args = parser.parse_args()
  result = register_app(args.name, args.author, args.sub_domain, host=args.host, description=args.description, framework=args.framework, deploy=args.deploy, memory=args.memory)
  print(result)