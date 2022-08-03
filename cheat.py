import argparse
import subprocess

def load_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search cheat.sh")
    parser.add_argument("lang", metavar="L", help="The topic to search for.")
    parser.add_argument("query", metavar="q", help="Search string")

    args = parser.parse_args()
    return args

def generate_query(query: str) -> str:
    return "+".join(query.split())

if __name__ == "__main__":
    args = load_args()
    query = generate_query(args.query)
    print(args.lang, query)
    command = ['curl', f'cht.sh/%s/{query}' % args.lang]
    subprocess.run(command)
    
