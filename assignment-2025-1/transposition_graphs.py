import argparse
from bts import run_bts
from graph import run_graph
from dfs import run_dfs

def main():
    parser = argparse.ArgumentParser(description="Transposition Graphs.")
    parser.add_argument("s", type=int, help="Number of 0s")
    parser.add_argument("t", type=int, help="Number of 1s")
    parser.add_argument("mode", choices=["graph", "bts", "dfs"],
                        help="Implementation mode")
    parser.add_argument("start", nargs="?", type=int, help="Starting node for dfs (decimal - optional)")
    args = parser.parse_args()

    if args.mode == "bts":
        run_bts(args.s, args.t)
    elif args.mode == "graph":
        run_graph(args.s, args.t)
    elif args.mode == "dfs":
        if args.start is not None:
            run_dfs(args.s, args.t, args.start)
        else:
            run_dfs(args.s, args.t)
    else:
        print(f"Unknown mode: {args.mode}")

if __name__ == "__main__":
    main()