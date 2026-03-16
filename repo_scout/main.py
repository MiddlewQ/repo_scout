from .cli import init_parser

def main() -> int:

    parser = init_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.debug:
        print(args)

    if args.verbose:
        print(f"Running {args.command}")
    args.func(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
