def load(hub, sources, cli=None, dyne_names=None, loader="yaml", parse_cli=True):
    """
    Load up the configs from the integrate system
    """
    if dyne_names is None:
        dyne_names = []
    raw = hub.config.dirs.load(sources, dyne_names, cli)
    os_vars = hub.config.os.init.gather(raw)
    cli_args, raw_cli = hub.config.args.gather(raw, cli, parse_cli)
    if cli_args.get("version"):
        hub.config.version.run(cli)
    configs = hub.config.file.init.parse(raw, cli, os_vars, cli_args, loader)
    opt = hub.config.order.apply(raw, raw_cli, cli, cli_args, os_vars, configs)
    hub.OPT = hub.pop.data.imap(opt)
