import os
import pprint
import platform

def main():
    env_var = os.environ

    print('The operating system version is ' + platform.platform())
    
    print("User Env Variables:")
    pprint.pprint(dict(env_var), width = 1) 

if __name__ == "__main__":
    main()