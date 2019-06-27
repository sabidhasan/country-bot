import os
""" Sets environment variable to whatever is specified """

def set_environ(value):
  os.environ["country_bot_env"] = value
  print("Setting OS environment to", value)
