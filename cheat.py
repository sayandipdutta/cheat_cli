import argparse
import subprocess
from dtypes import Commands, Options, SearchOpts


def load_args() -> argparse.Namespace:
    """
    Load arguments from command line.

    Returns:
        argparse.Namespace object containing all the options.
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
    commands = frozenset[Commands]([
        "help",
        "list",
        "post",
        "bash_completion",
        "styles",
        "styles_demo",
        "random",
    ])
    """set of available commands"""
    options = frozenset[Options]([
        "q",
        "T",
        "Q",
    ])
    """set of available options"""
    searchopts = frozenset[SearchOpts]([
        "b",
        "i",
        "r",
    ])
    """set of available searchopts"""


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

        Arguments:
            topic: str (default: None) -> topic to search for.
            subtopic: str (default: None) -> subtopic to search for. *
            keywords: list[str] (default: None) -> keyword(s) to search for. *
            cmd: Commands (default: None) -> One of the following special commands- * **
                "help", "list", "post", "bash_completion", "styles", "styles-demo", "random"
            options: list[Options] (default: None) -> One of the following options- **
                "q", "T", "Q"
            style: str (default: None) -> Any style to apply to output.
            search_opts: list[SearchOpts] -> One of the following search options- **
                "b", "i", "r"

        * NOTE:
            subtopic, keywords, and, cmd are mutually exclusive. Only one should be provided.
            If any two are not None, a ValueError is raised.
        ** NOTE:
            Anything other than the allowed values raise ValueError.

        Returns:
                A tuple consisting of list of formated arguments, and the formatted query 
            to be used to search cheat.sh.

        Example:
            >>> from cheat import Cheat
            >>> args, query = Cheat.format_args(
            ...     "python", kwd=["iter", "next"],
            ...     cmd="help", options=["Q", "T"]
            ... )
            Traceback (most recent call last):
                ...
            ValueError: Only one out of subtopic, kwd, and cmd may be provided. Got 2.

            >>> args, query = format_args(
            ...     "python", kwd=["iter", "next"],
            ...     options=["Q", "T"], style="bw"
            ... )
            >>> args
            ['/python', '', '/~iter~next', '', '?QT', '&style=bw', '']
            >>> query
            '/python/~iter~next?QT&style=bw'
        """

        if (n := sum(arg is not None for arg in [subtopic, kwd, cmd])) > 1:
            raise ValueError(f"Only one out of subtopic, kwd, and, cmd may be provided. Got {n}.")

        if options is not None and not Cheat.options.issuperset(options):
            try:
                raise ValueError("Invalid value for options.")
            except ValueError as error:
                error.add_note(f"Hint: Try one of {', '.join(Cheat.options)}.")
                raise

        if cmd is not None and cmd not in Cheat.commands:
            try:
                raise ValueError("Invalid value for cmd.")
            except ValueError as error:
                error.add_note(f"Hint: Try one of {', '.join(Cheat.commands)}.")
                raise

        if search_opts is not None and not Cheat.searchopts.issuperset(search_opts):
            try:
                raise ValueError("Invalid value for search options.")
            except ValueError as error:
                error.add_note(f"Hint: Try one of {', '.join(Cheat.searchopts)}.")
                raise

        topic = ("/"+ "+".join(topic.strip().split())) if topic else ""
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
    
