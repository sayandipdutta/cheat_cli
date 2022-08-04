import argparse
import subprocess
from dtypes import Commands, Options, SearchOpts

def load_args() -> argparse.Namespace:
    """
    Load arguments from command line.
    """
    parser = argparse.ArgumentParser(description="Search cheat.sh")
    group = parser.add_mutually_exclusive_group()
    add_args = parser.add_argument
    add_args("topic", metavar="L", help="The topic to search for.")
    group.add_argument("-s", "--subtopic", metavar="q", help="Search string")
    group.add_argument("-k", "--kwd", help="Keywords", nargs='*')
    group.add_argument("-c", "--cmd", choices=list(Cheat.commands))
    add_args("-o", "--options", nargs='*', choices=list(Cheat.options))
    add_args("--style")
    add_args("--search_opts", nargs=True, choices=list(Cheat.searchopts))

    args = parser.parse_args()
    return args

class Cheat:
    commands: frozenset[Commands] = frozenset([
        "help",
        "list",
        "post",
        "bash_completion",
        "styles",
        "styles_demo",
        "random",
    ])

    options: frozenset[Options] = frozenset([
        "q",
        "T",
        "Q",
    ])

    searchopts: frozenset[SearchOpts] = frozenset([
        "b",
        "i",
        "r",
    ])


    @staticmethod
    def format_args(
            topic: str = None,
            *,
            subtopic: str = None,
            kwd: list[str] = None,
            cmd: Commands = None,
            options: list[Options] = None,
            style: str = None,
            search_opts: list[SearchOpts] = None,
            ) -> tuple[list[str], str]:
        """
        Format arguments as per cheat.sh requirement.
        """
        topic = "/"+ "+".join(topic.strip().split())
        subtopic = '/' + "+".join(subtopic.strip().split()) if subtopic else ""
        cmds = '/:%s' % cmd if cmd else ''
        opts = ("?"+"".join(options)) if options else ""
        style = ("&style=%s" % style) if style else ""
        search_opt = ("/" + "".join(search_opts)) if search_opts else ''
        keywords = ("/~" + "~".join(kwd)) if kwd else ""
        args = [topic, subtopic, keywords, cmds, opts, style, search_opt]
        query = ''.join(args)
        return args, query


if __name__ == "__main__":
    args = load_args()
    formatted_args, query = Cheat.format_args(
            topic=args.topic,
            subtopic=args.subtopic,
            cmd=args.cmd,
            options=args.options,
            style=args.style,
            search_opts=args.search_opts,
            kwd=args.kwd
        )
    command = ['curl', f'cht.sh%s' %  query]
    print(args, query, command)
    subprocess.run(command)
    
