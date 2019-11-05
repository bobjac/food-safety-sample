import os
import pprint

def main():
    env_var = os.environ

    print("User Env Variables:")
    pprint.pprint(dict(env_var), width = 1) 

if __name__ == "__main__":
    main()