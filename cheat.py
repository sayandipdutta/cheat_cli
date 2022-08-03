import argparse
import subprocess

class Cheat:
    cmds = (
        "help",               # help page
        "list",               # list all cheat sheets
        "post",               # how to post new cheat sheet
        "bash_completion",    # bash function for tab completion
        "styles",             # list of color styles
        "styles_demo",        # show color styles usage examples
        "random",             # fetches a random cheat sheet
    )

    options = (
        "q",                  # quiet mode, don't show github/twitter buttons
        "T",                  # text only, no ANSI sequences
        "c",                  # do not comment text, do not shift code (QUERY+ only)
        "C",                  # do not comment text, shift code (QUERY+ only)
        "Q",                  # code only, don't show text (QUERY+ only)
    )
    search_opts = ('b', 'i', 'r')


def load_args() -> argparse.Namespace:
    cmds = Cheat.cmds
    options = Cheat.options
    search_opts = Cheat.search_opts
    parser = argparse.ArgumentParser(description="Search cheat.sh")
    add_args = parser.add_argument
    add_args("topic", metavar="L", help="The topic to search for.")
    add_args("subtopic", metavar="q", help="Search string")
    add_args("-c", "--cmd", choices=cmds, help=f"One of the following commands: {', '.join(cmds)}")
    add_args("-k", "--kwd", help="Keywords", nargs='*')
    add_args("-o", "--options", nargs='*', choices=options)
    add_args("-s", "--style")
    add_args("--search_opts", nargs=True, choices=search_opts)

    args = parser.parse_args()
    return args

def generate_query() -> str:
    args = load_args()
    topic = "/"+ "+".join(args.topic.strip().split())
    subtopic = '/' + "+".join(args.subtopic.strip().split()) 
    cmd = '/:%s' % args.cmd if args.cmd else ''
    opts = ("?"+"".join(args.options)) if args.options else ""
    style = ("&style=%s" % args.style) if args.style else ""
    search_opts = ("/" + "".join(args.search_opts)) if args.search_opts else ''
    keywords = ("/~" + "~".join(args.kwd)) if args.kwd else ""
    query = topic + subtopic + keywords + cmd + opts + style + search_opts
    return query

if __name__ == "__main__":
    args = load_args()
    query = generate_query()
    command = ['curl', f'cht.sh%s' %  query]
    print(args, query, command)
    subprocess.run(command)
    
