import sys
from resultsdb_frontend import cli

if __name__ == '__main__':
    exit = cli.main()
    if exit:
        sys.exit(exit)

