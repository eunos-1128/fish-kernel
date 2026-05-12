import json
import shutil
import socket
import sys
import tempfile
from pathlib import Path

import pytest
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager


def _can_bind_local_socket() -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", 0))
    except OSError:
        return False
    finally:
        sock.close()
    return True


def _execute_and_collect(client, code: str, timeout: float = 30.0) -> dict:
    msg_id = client.execute(code)
    stdout_parts = []
    errors = []

    while True:
        msg = client.get_iopub_msg(timeout=timeout)
        if msg.get("parent_header", {}).get("msg_id") != msg_id:
            continue

        msg_type = msg["header"]["msg_type"]
        content = msg["content"]
        if msg_type == "stream":
            stdout_parts.append(content.get("text", ""))
        elif msg_type == "error":
            errors.append(content)
        elif msg_type == "status" and content.get("execution_state") == "idle":
            break

    while True:
        shell_msg = client.get_shell_msg(timeout=timeout)
        if shell_msg.get("parent_header", {}).get("msg_id") == msg_id:
            shell_content = shell_msg["content"]
            break

    return {
        "stdout": "".join(stdout_parts),
        "errors": errors,
        "shell_content": shell_content,
    }


@pytest.fixture(scope="module")
def fish_kernel_client():
    if shutil.which("fish") is None:
        pytest.skip("fish is not installed on PATH")
    if not _can_bind_local_socket():
        pytest.skip("Local socket binding is not available in this environment")

    with tempfile.TemporaryDirectory() as td:
        kernel_root = Path(td) / "kernels"
        kernel_dir = kernel_root / "fish-e2e"
        kernel_dir.mkdir(parents=True, exist_ok=True)

        kernel_json = {
            "argv": [sys.executable, "-m", "fish_kernel", "-f", "{connection_file}"],
            "display_name": "Fish E2E",
            "language": "fish",
        }
        (kernel_dir / "kernel.json").write_text(
            json.dumps(kernel_json), encoding="utf-8"
        )

        ksm = KernelSpecManager()
        ksm.kernel_dirs = [str(kernel_root), *ksm.kernel_dirs]
        km = KernelManager(kernel_name="fish-e2e", kernel_spec_manager=ksm)
        try:
            km.start_kernel()
        except OSError as exc:
            pytest.skip(f"Unable to start kernel in this environment: {exc}")

        client = km.client()
        client.start_channels()
        try:
            client.wait_for_ready(timeout=30)
            yield client
        finally:
            client.stop_channels()
            km.shutdown_kernel(now=True)


def test_e2e_execute_math(fish_kernel_client):
    result = _execute_and_collect(fish_kernel_client, "math 1+1")

    assert result["shell_content"]["status"] == "ok"
    assert result["errors"] == []
    assert "2" in result["stdout"]


def test_e2e_execute_failure_returns_error(fish_kernel_client):
    result = _execute_and_collect(fish_kernel_client, "false")

    assert result["shell_content"]["status"] == "error"
    assert result["errors"] != []
    assert result["errors"][0]["evalue"] == "1"
