import yaml
import os

DEFAULT_CONFIG_PATH = "config/config.yml"

class InvalidConfigException(Exception):
  def __init__(self, message):
    self.message = f"[config error] {message}"

class InvalidStructureException(Exception):
  def __init__(self, message):
    self.message = f"[structure error] {message}"

class InvalidAppConfigException(Exception):
  def __init__(self, message):
    self.message = f"[app param error] {message}"

def validate_config(config_object):
  if not config_object["store_version"]:
    raise InvalidConfigException("store version not specified")
  if not config_object["port"]:
    raise InvalidConfigException("store port not specified")
  if config_object["apps"] is None:
    raise InvalidConfigException("store apps not specified")
  
  names = set()
  sub_domains = set()
  for idx, app in enumerate(config_object["apps"]):
    if not app["name"]:
      raise InvalidConfigException(f"app with index {idx} does not specify app name")
    if app["name"] == "placeholder":
      continue
    if app["name"] in names:
      raise InvalidConfigException(f"app name \"{app['name']}\" has duplication")
    names.add(app["name"])
    if not app["author"]:
      raise InvalidConfigException(f"app \"{app['name']}\" did not specify author")
    if not app["host"]:
      raise InvalidConfigException(f"app \"{app['name']}\" did not specify host")
    if not app["sub_domain"]:
      raise InvalidConfigException(f"app \"{app['name']}\" did not specify sub domain")
    if app["sub_domain"] in sub_domains:
      raise InvalidConfigException(f"sub domain \"{app['sub_domain']}\" has duplication")

def validate_config_yaml(path=DEFAULT_CONFIG_PATH):
  if not os.path.exists(path):
    raise InvalidConfigException("cannot file config file")
  with open(path, 'r') as config_file:
    config_object = yaml.safe_load(config_file)
    validate_config(config_object)

def validate_structure(config_object=None, config_path=DEFAULT_CONFIG_PATH):
  config_file = open(config_path, 'r')
  if not config_object:
    config_object = yaml.safe_load(config_file)

  if not os.path.exists("sub_projects"):
    raise InvalidStructureException("must have \"sub_project\" folder")
  if not os.path.exists(config_path):
    raise InvalidStructureException("cannot file config file")

  apps = config_object["apps"]
  if not apps:
    raise InvalidConfigException("store apps not specified")
  for app in apps:
    if not app["sub_domain"]:
      raise InvalidConfigException(f"app \"{app['name']}\" did not specify sub domain")
    if app["sub_domain"] == "placeholder":
      continue
    if not os.path.exists(f"sub_projects/{app['sub_domain']}"):
      raise InvalidStructureException(f"sub domain \"{app['sub_domain']} does not exist\"")
  config_file.close()

def validate():
  validate_config_yaml()
  validate_structure()

def add_new_app(config_object, app_name, app_author, app_sub_domain, app_host="localhost", app_description="description placeholder"):
  for app in config_object["apps"]:
    if app["name"] == "placeholder":
      config_object["apps"] = []
      break
  
  config_object["apps"].append({ "name": app_name, "author": app_author, "sub_domain": app_sub_domain, "host": app_host, "description": app_description })
  validate_config(config_object)

  if not os.path.exists("sub_projects"):
    os.mkdir("sub_projects")
  
  if not os.path.exists(f"sub_projects/{app_sub_domain}"):
    os.mkdir(f"sub_projects/{app_sub_domain}")

  validate_structure(config_object=config_object)
  prepare_basic_structure()

def prepare_basic_structure():
  pass

validate()