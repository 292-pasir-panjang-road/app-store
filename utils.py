import yaml
import os
import shutil

DEFAULT_CONFIG_PATH = "config/config.yml"
PLACEHOLDER_APP = { "name": "placeholder", "sub_domain": "placeholder", "host": "placeholder", "port": "placeholder", "author": "placeholder", "description": "placeholder", "framework": "placeholder", "deploy": "placeholder", "memory": "placeholder" }
AVAILABLE_FRAMEWORKS = ["flask"]

#######################################
#                                     #
#      Defines Error / Exceptions     #
#                                     #
#######################################
class Error(Exception):
  def __init__(self, message):
    self.message = message

class InvalidConfigError(Error):
  def __init__(self, message):
    self.message = f"[config error] {message}"

class InvalidStructureError(Error):
  def __init__(self, message):
    self.message = f"[structure error] {message}"

class InvalidAppConfigError(Error):
  def __init__(self, message):
    self.message = f"[app param error] {message}"

#######################################
#                                     #
#     Defines validation functions    #
#                                     #
#######################################
def validate_config(config_object):
  if not config_object["store_version"]:
    raise InvalidConfigError("store version not specified")
  if not config_object["port"]:
    raise InvalidConfigError("store port not specified")
  if config_object["apps"] is None:
    raise InvalidConfigError("store apps not specified")
  
  # rules:
  # 1. name, author, host, port, sub domain and framework must exist
  # 2. name, port, sub domain cannot have duplication
  names = set()
  ports = set()
  sub_domains = set()
  for idx, app in enumerate(config_object["apps"]):
    # check name
    if "name" not in app or not app["name"]:
      raise InvalidConfigError(f"app with index {idx} does not specify app name")
    if app["name"] == "placeholder":
      continue
    if app["name"] in names:
      raise InvalidConfigError(f"app name \"{app['name']}\" has duplication")
    names.add(app["name"])
    
    # check author
    if "author" not in app or not app["author"]:
      raise InvalidConfigError(f"app \"{app['name']}\" did not specify author")
    
    # check host
    if "host" not in app or not app["host"]:
      raise InvalidConfigError(f"app \"{app['name']}\" did not specify host")
    
    # check port
    if "port" not in app or not app["port"]:
      raise InvalidConfigError("app port not specified")
    if app["host"] == "localhost" and app["port"] in ports:
      raise InvalidConfigError(f"port \"{app['port']}\" has been occupied")
    if app["host"] == "localhost":
      ports.add(app["port"])
    
    # check sub domain
    if "sub_domain" not in app or not app["sub_domain"]:
      raise InvalidConfigError(f"app \"{app['name']}\" did not specify sub domain")
    if app["sub_domain"] in sub_domains:
      raise InvalidConfigError(f"sub domain \"{app['sub_domain']}\" has duplication")
    sub_domains.add(app["sub_domain"])
    
    # check framework
    if "framework" not in app or not app["framework"]:
      raise InvalidConfigError("framework not specified")
    if app["framework"] not in AVAILABLE_FRAMEWORKS:
      raise InvalidConfigError(f"framework \"{app['framework']}\" not available now")

    # check deploy
    if "deploy" not in app:
      raise InvalidConfigError("deploy status not specified")
    
    # check memory
    if "memory" not in app:
      raise InvalidConfigError("memory not specified")

def validate_config_yaml(path=DEFAULT_CONFIG_PATH):
  if not os.path.exists(path):
    raise InvalidConfigError("cannot file config file")
  with open(path, 'r') as config_file:
    config_object = yaml.safe_load(config_file)
    validate_config(config_object)

def validate_structure(config_object=None, config_path=DEFAULT_CONFIG_PATH):
  config_file = open(config_path, 'r')
  if not config_object:
    config_object = yaml.safe_load(config_file)

  # must have sub projects folder
  if not os.path.exists("sub_projects"):
    os.mkdir("sub_projects")
  if not os.path.exists(config_path):
    raise InvalidStructureError("cannot file config file")

  # just o ensure all he registered app have corresponding sub dir
  apps = config_object["apps"]
  if not apps:
    raise InvalidConfigError("store apps not specified")
  for app in apps:
    if "sub_domain" not in app or not app["sub_domain"]:
      raise InvalidConfigError(f"app \"{app['name']}\" did not specify sub domain")
    if app["sub_domain"] == "placeholder":
      continue
    if not os.path.exists(f"sub_projects/{app['sub_domain']}"):
      raise InvalidStructureError(f"sub domain \"{app['sub_domain']}\" does not exist")
  config_file.close()

#######################################
#                                     #
#         App create / remove         #
#                                     #
#######################################
def prepare_basic_structure(sub_domain, framework):
  # move template files into corresponding app diretory
  if not os.path.exists(f"sub_projects/{sub_domain}"):
    os.mkdir(f"sub_projects/{sub_domain}")
  
  for file_name in os.listdir(f"templates/{framework}"):
    shutil.copyfile(f"templates/{framework}/{file_name}", f"sub_projects/{sub_domain}/{file_name.replace('.template', '')}")

def add_new_app(config_object, app_name, app_author, app_sub_domain, app_host, app_description, framework, deploy, memory):
  current_max_port = 8000
  for app in config_object["apps"]:
    if app["name"] == "placeholder":
      config_object["apps"] = []
      break
    current_max_port = max(current_max_port, app["port"])
  
  config_object["apps"].append({ "name": app_name, "author": app_author, "sub_domain": app_sub_domain, "host": app_host, "port": current_max_port + 1, "description": app_description, "framework": framework, "deploy": deploy, "memory": memory })
  validate_config(config_object)
  
  prepare_basic_structure(app_sub_domain, framework)
  validate_structure(config_object=config_object)
  return config_object

def register_app(name, author, sub_domain, host="localhost", description="description placeholder", framework="flask", deploy=False, memory=256):
  try:
    with open("config/config.yml", "r") as config_file:
      config_object = yaml.safe_load(config_file)
      result_config = add_new_app(config_object, name, author, sub_domain, host, description, framework, deploy, memory)
      with open("config/config.yml.tmp", "w") as temp_config:
        yaml.safe_dump(result_config, temp_config)
    
    os.replace("config/config.yml.tmp", "config/config.yml")
    return "create success"
  except Error as e:
    return e.message

def remove_app(sub_domain):
  with open("config/config.yml", "r") as config_file:
    config_object = yaml.safe_load(config_file)
    new_apps = list(filter(lambda app: app["sub_domain"] != sub_domain, config_object["apps"]))
    if not new_apps:
      new_apps.append(PLACEHOLDER_APP)
    config_object["apps"] = new_apps
    if os.path.exists(f"sub_projects/{sub_domain}"):
      shutil.rmtree(f"sub_projects/{sub_domain}")
    with open("config/config.yml.tmp", "w") as temp_config:
        yaml.safe_dump(config_object, temp_config)
    os.replace("config/config.yml.tmp", "config/config.yml")
    return "remove success"

def build_apps(tag):
  with open("config/config.yml", "r") as config_file:
    config_object = yaml.safe_load(config_file)
    commands = []
    for app in config_object["apps"]:
      if app["name"] == "placeholder":
        continue
      # currently do not support other deploy method
      if app["host"] != "localhost":
        continue
      if not app["deploy"]:
        continue
      commands.append(f"docker build -t {app['sub_domain']} ./sub_projects/{app['sub_domain']}/ && docker tag {app['sub_domain']} $DOCKER_USERNAME/{app['sub_domain']}:{tag} && docker push $DOCKER_USERNAME/{app['sub_domain']}:{tag}")
  commands_str = " ; ".join(commands)
  print(commands_str)
  os.system(commands_str)

def get_app_deploy_command(app_config_object, tag):
  sub_domain = app_config_object["sub_domain"]
  port = app_config_object["port"]
  cmd = f"sudo docker stop 292ppr/{sub_domain}; sudo docker pull 292ppr/{sub_domain} && sudo docker run --name=292ppr/{sub_domain} -it --rm -p {port}:8000 292ppr/{sub_domain}:{tag}"
  return cmd

def deploy_apps(tag):
  with open("config/config.yml", "r") as config_file:
    config_object = yaml.safe_load(config_file)
    commands = []
    for app in config_object["apps"]:
      if app["name"] == "placeholder":
        continue
      if app["host"] != "localhost":
        continue
      if not app["deploy"]:
        continue
      commands.append(get_app_deploy_command(app, tag))
    docker_cmd = " ; ".join(commands)
    cmd = f"ssh 292ppr@$DEPLOY_HOST <<EOF {docker_cmd} EOF"
    print(cmd)
    os.system(cmd)

def validate():
  try:
    validate_config_yaml()
    validate_structure()
    exit(0)
  except Error as e:
    print(e.message)
    exit(1)

if __name__ == "__main__":
  validate()