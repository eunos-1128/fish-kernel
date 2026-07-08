import sys

import fish_kernel.install as install
import fish_kernel.remove as remove


def test_main_default_removes_with_no_scope(monkeypatch):
    observed = {}

    def fake_remove_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix
        return "/path/to/fish"

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main([])

    assert exit_code == 0
    assert observed == {"user": False, "prefix": None}


def test_main_user_calls_remover(monkeypatch):
    observed = {}

    def fake_remove_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main(["--user"])

    assert exit_code == 0
    assert observed == {"user": True, "prefix": None}


def test_main_sys_prefix_calls_remover(monkeypatch):
    observed = {}

    def fake_remove_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main(["--sys-prefix"])

    assert exit_code == 0
    assert observed == {"user": False, "prefix": sys.prefix}


def test_main_prefix_calls_remover(monkeypatch):
    observed = {}

    def fake_remove_my_kernel_spec(*, user, prefix):
        observed["user"] = user
        observed["prefix"] = prefix

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main(["--prefix", "/tmp/custom-prefix"])

    assert exit_code == 0
    assert observed == {"user": False, "prefix": "/tmp/custom-prefix"}


def test_main_user_and_prefix_are_mutually_exclusive(capsys):
    exit_code = None
    try:
        remove.main(["--user", "--prefix", "/tmp/custom-prefix"])
    except SystemExit as e:
        exit_code = e.code
    err = capsys.readouterr().err

    assert exit_code == 2
    assert "not allowed with argument" in err


def test_main_missing_kernel_spec_returns_1(monkeypatch, capsys):
    def fake_remove_my_kernel_spec(*, user, prefix):
        raise KeyError(remove.KERNEL_NAME)

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main([])
    err = capsys.readouterr().err

    assert exit_code == 1
    assert "No such kernel spec installed" in err
    assert "for" not in err


def test_main_missing_kernel_spec_mentions_scope(monkeypatch, capsys):
    def fake_remove_my_kernel_spec(*, user, prefix):
        raise KeyError(remove.KERNEL_NAME)

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main(["--user"])
    err = capsys.readouterr().err

    assert exit_code == 1
    assert "No such kernel spec installed for user" in err


def test_main_permission_error_returns_1(monkeypatch, capsys):
    def fake_remove_my_kernel_spec(*, user, prefix):
        raise PermissionError("denied")

    monkeypatch.setattr(remove, "remove_my_kernel_spec", fake_remove_my_kernel_spec)

    exit_code = remove.main([])
    err = capsys.readouterr().err

    assert exit_code == 1
    assert "denied" in err
    assert "sudo" in err


def test_main_help_lists_scope_options(capsys):
    exit_code = None
    try:
        remove.main(["--help"])
    except SystemExit as e:
        exit_code = e.code
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "usage:" in out
    assert "--user" in out
    assert "--sys-prefix" in out
    assert "--prefix" in out


def test_remove_scoped_to_prefix_leaves_other_prefix_untouched(tmp_path):
    prefix_a = tmp_path / "a"
    prefix_b = tmp_path / "b"
    prefix_a.mkdir()
    prefix_b.mkdir()

    install.install_my_kernel_spec(user=False, prefix=str(prefix_a))
    install.install_my_kernel_spec(user=False, prefix=str(prefix_b))

    kernel_dir_a = prefix_a / "share" / "jupyter" / "kernels" / "fish"
    kernel_dir_b = prefix_b / "share" / "jupyter" / "kernels" / "fish"
    assert kernel_dir_a.is_dir()
    assert kernel_dir_b.is_dir()

    remove.remove_my_kernel_spec(user=False, prefix=str(prefix_a))

    assert not kernel_dir_a.exists()
    assert kernel_dir_b.is_dir()

    # Clean up the still-installed copy so the test leaves no side effects.
    remove.remove_my_kernel_spec(user=False, prefix=str(prefix_b))
    assert not kernel_dir_b.exists()


def test_remove_scoped_to_prefix_raises_keyerror_when_absent(tmp_path):
    prefix = tmp_path / "empty-prefix"
    prefix.mkdir()

    try:
        remove.remove_my_kernel_spec(user=False, prefix=str(prefix))
    except KeyError:
        pass
    else:
        raise AssertionError("Expected KeyError for a prefix with no fish kernel spec")
