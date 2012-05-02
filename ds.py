


import getopt, sys

import Backend

cmds = [
        ("command", "Append command to pending list"),
        ("-g group command", "Restrict command to this group's privileges"),
        ("-p cmdid command", "Require this command to run before command can be run"),
        ("-a cmdid", "Approve command"),
        ("-r cmdid", "Remove command"),
        ("-l [cmdid]", "List commands requiring approval"),
        ("-lv [cmdid]", "List with further details"),
        ("-d [backend]", "Create new database. Optionally specify backend.")
        ]

def groupusers():
    import grp
    return { g.gr_name : set(g.gr_mem) for g in grp.getgrall() }

def main():

    import argparse

    parser = argparse.ArgumentParser(description='Dual authorise commands.')
    parser.add_argument('cmd', nargs=argparse.REMAINDER,
                       help='Command to put into pending bucket')
    parser.add_argument('-a', '--approve', type=int, metavar='cmdid', nargs=1,
                       help='Command to approve from pending bucket')
    parser.add_argument('-r', '--remove', type=int, metavar='cmdid', nargs=1,
                       help='Command to remove from pending bucket')
    parser.add_argument('-g', '--groups', metavar='grp', nargs='+',
                       help='Run with these groups'' privileges')
    parser.add_argument('-p', '--prerequisite', metavar='cmdid', nargs='?',
                       help='Only allow the running of command once this command has run.'\
                            'The command is specified by the cmdid')
    parser.add_argument('-l', '--list', metavar='cmdid', nargs='?',
                         type=int, default=0,
                         help='List details')
    parser.add_argument('-c', '--createbackend', metavar='backend', nargs='?', default=0,
                       help='Create new database. Optionally specify backend.')

    args = parser.parse_args()

    import json

    cfg = json.load(open("config.json"))

    import getpass
    
    uid = getpass.getuser()

    if args.createbackend is None:
        b = Backend.Backend("test",cfg,new=True)
        exit(1)

    b = Backend.Backend("test",cfg)


    if args.approve:
        print b.approveCommand(args.approve, uid)

    elif args.cmd:
        b.addCommand(" ".join(args.cmd), uid)

    elif args.remove:
        b.removeCommand(args.remove, uid)

    elif args.list is None:
        print b.getPendingCommands(args.list)

    exit(1)


if __name__ == "__main__":
    main()


# vim: set expandtab sw=4 ts=4:
