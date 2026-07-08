import fish_kernel.cli as cli


def test_main_help_shows_usage(capsys):
    exit_code = cli.main([])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "usage: fish-kernel <command> [options]" in out


def test_main_version_prints_version(capsys):
    exit_code = cli.main(["--version"])
    out = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert out == cli.__version__


def test_main_unknown_command_returns_error(capsys):
    exit_code = cli.main(["unknown"])
    err = capsys.readouterr().err

    assert exit_code == 2
    assert "Unknown command: unknown" in err


def test_main_install_delegates_to_install_module(monkeypatch):
    observed = {}

    def fake_install_main(args):
        observed["args"] = args
        return 7

    monkeypatch.setattr(cli, "install_main", fake_install_main)

    exit_code = cli.main(["install", "--user"])

    assert exit_code == 7
    assert observed["args"] == ["--user"]


def test_main_add_delegates_to_install_module(monkeypatch):
    observed = {}

    def fake_install_main(args):
        observed["args"] = args
        return 7

    monkeypatch.setattr(cli, "install_main", fake_install_main)

    exit_code = cli.main(["add", "--user"])

    assert exit_code == 7
    assert observed["args"] == ["--user"]


def test_main_remove_delegates_to_remove_module(monkeypatch):
    observed = {}

    def fake_remove_main(args):
        observed["args"] = args
        return 3

    monkeypatch.setattr(cli, "remove_main", fake_remove_main)

    exit_code = cli.main(["remove"])

    assert exit_code == 3
    assert observed["args"] == []


def test_main_uninstall_delegates_to_remove_module(monkeypatch):
    observed = {}

    def fake_remove_main(args):
        observed["args"] = args
        return 3

    monkeypatch.setattr(cli, "remove_main", fake_remove_main)

    exit_code = cli.main(["uninstall"])

    assert exit_code == 3
    assert observed["args"] == []
