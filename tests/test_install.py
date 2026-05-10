import sys

import fish_kernel.install as install


def test_main_without_target_option_prints_help_and_returns_2(capsys):
    exit_code = install.main([])
    out = capsys.readouterr().out

    assert exit_code == 2
    assert "usage:" in out
    assert "--user" in out
    assert "--sys-prefix" in out
    assert "--prefix" in out


def test_main_user_calls_installer(monkeypatch):
    observed = {}

    def fake_install_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(install, "install_my_kernel_spec", fake_install_my_kernel_spec)

    exit_code = install.main(["--user"])

    assert exit_code == 0
    assert observed == {"user": True, "prefix": None}


def test_main_sys_prefix_calls_installer(monkeypatch):
    observed = {}

    def fake_install_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(install, "install_my_kernel_spec", fake_install_my_kernel_spec)

    exit_code = install.main(["--sys-prefix"])

    assert exit_code == 0
    assert observed == {"user": False, "prefix": sys.prefix}


def test_main_prefix_calls_installer(monkeypatch):
    observed = {}

    def fake_install_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(install, "install_my_kernel_spec", fake_install_my_kernel_spec)

    exit_code = install.main(["--prefix", "/tmp/custom-prefix"])

    assert exit_code == 0
    assert observed == {"user": False, "prefix": "/tmp/custom-prefix"}
