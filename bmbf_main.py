import generate_bmbf_list
import databaseConnect
import config
from pprint import pprint


if __name__ == "__main__":
    if (config.use_db):
        generate_bmbf_list.mainDB(1)
    else:
        generate_bmbf_list.mainFiles()