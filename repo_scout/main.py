from .cli import init_parser

def main():

    parser = init_parser()
    args = parser.parse_args()

    if args.verbose:
        print(args)

    if args.command is None:
        parser.print_help()
        raise SystemExit(0)

    args.func(args)

if __name__ == "__main__":
    main()
