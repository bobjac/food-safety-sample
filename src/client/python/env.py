import os
import pprint
import platform
import yaml

def main():
    z = add(4, 5)
    print("The result of add is %s"  %z)

    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    for section in cfg:
        print(section)

    print(cfg['iothub'])
    print(cfg['other'])

    print(cfg['iothub']['connectionstring'])

    env_var = os.environ

    print('The operating system version is ' + platform.platform())
    
    print("User Env Variables:")
    pprint.pprint(dict(env_var), width = 1) 

def add(x, y):
    return x + y

if __name__ == "__main__":
    main()