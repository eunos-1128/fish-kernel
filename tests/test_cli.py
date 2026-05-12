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
