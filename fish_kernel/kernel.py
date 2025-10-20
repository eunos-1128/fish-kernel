import os
import pathlib
import random
import re
import shlex
import signal
import string
import tempfile
from subprocess import check_output

import pexpect
from ipykernel.kernelbase import Kernel
from pexpect import EOF

from . import __version__
from .display import build_cmds, extract_contents, split_lines

version_pat = re.compile(r"version (\d+(\.\d+)+)")
_ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
_OSC_ESCAPE_RE = re.compile(r"\x1B\][^\x07\x1B]*(?:\x07|\x1B\\)")
_DCS_ESCAPE_RE = re.compile(r"\x1BP.*?\x1B\\", re.DOTALL)


def _strip_control_sequences(text):
    text = _OSC_ESCAPE_RE.sub("", text)
    text = _DCS_ESCAPE_RE.sub("", text)
    text = _ANSI_ESCAPE_RE.sub("", text)
    # Fallback for non-standard two-byte escape sequences.
    return re.sub(r"\x1B.", "", text)


class _FishSession:
    """Persistent fish process that executes commands via temporary sourced files."""

    def __init__(self, prompt_prefix):
        fish_env = os.environ.copy()
        fish_env["FISH_KERNEL_PROMPT"] = prompt_prefix
        init_script = pathlib.Path(__file__).with_name("init_config.fish")
        source_init_cmd = f"source {shlex.quote(str(init_script))}"
        self.child = pexpect.spawn(
            "fish",
            [
                "--no-config",
                "--features",
                "no-mark-prompt,no-query-term",
                "--interactive",
                "--init-command",
                source_init_cmd,
            ],
            echo=False,
            env=fish_env,
            encoding="utf-8",
            codec_errors="replace",
        )
        self.prompt_prefix = prompt_prefix

        self.run_command("set -gx PAGER cat", timeout=10)
        self.run_command(build_cmds(), timeout=10)

    def close(self):
        if self.child.isalive():
            self.child.terminate(force=True)

    def _write_temp_script(self, command, prefix):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".fish", prefix=prefix, delete=False
        ) as tmp:
            temp_path = pathlib.Path(tmp.name)
            tmp.write(command)
            if not command.endswith("\n"):
                tmp.write("\n")
        return temp_path

    def _wrap_source_command(self, source_cmd):
        rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        status_tag = f"__FISH_KERNEL_STATUS_{rand}__"
        done_tag = f"__FISH_KERNEL_DONE_{rand}__"

        wrapped_script = (
            f"{source_cmd}; "
            f"set -l __fish_kernel_status $status; "
            f"printf '%s%s\\n' '{status_tag}' $__fish_kernel_status; "
            f"printf '%s\\n' '{done_tag}'"
        )
        return wrapped_script, status_tag, done_tag

    def _parse_output(self, raw_output, status_tag, noise_tokens):
        output_lines = []
        status = 1

        cleaned = _strip_control_sequences(raw_output)
        for line in split_lines(cleaned):
            line_no_ending = line.rstrip("\r\n")
            compact = line_no_ending.strip()
            if line_no_ending.startswith(status_tag):
                status_text = line_no_ending[len(status_tag) :].strip()
                if re.fullmatch(r"-?\d+", status_text):
                    status = int(status_text)
                continue
            if compact.startswith(self.prompt_prefix.strip()):
                continue
            if compact in {"source", "⏎"}:
                continue
            if compact.replace(" ", "") == "⏎":
                continue
            if any(token in compact for token in noise_tokens):
                continue
            output_lines.append(line)

        while output_lines and output_lines[0].strip() == "":
            output_lines.pop(0)

        return "".join(output_lines).replace("\r", ""), status

    def run_command(self, command, timeout=-1):
        if command is None:
            raise ValueError("No command was given")

        command_path = self._write_temp_script(command, prefix="fish_kernel_cmd_")
        command_source_cmd = f"source {shlex.quote(str(command_path))}"
        wrapped_script, status_tag, done_tag = self._wrap_source_command(
            command_source_cmd
        )
        wrapper_path = self._write_temp_script(
            wrapped_script, prefix="fish_kernel_wrap_"
        )
        wrapper_source_cmd = f"source {shlex.quote(str(wrapper_path))}"
        noise_tokens = {
            str(command_path),
            str(wrapper_path),
            "fish_kernel_wrap_",
            "fish_kernel_cmd_",
        }

        try:
            self.child.sendline(wrapper_source_cmd)
            expect_timeout = self.child.timeout if timeout == -1 else timeout
            self.child.expect(re.escape(done_tag), timeout=expect_timeout)
            raw_output = self.child.before
        finally:
            wrapper_path.unlink(missing_ok=True)
            command_path.unlink(missing_ok=True)

        return self._parse_output(raw_output, status_tag, noise_tokens)


class FishKernel(Kernel):
    implementation = "fish-kernel"
    implementation_version = __version__

    @property
    def language_version(self):
        m = version_pat.search(self.banner)
        return m.group(1)

    _banner = None

    @property
    def banner(self):
        if self._banner is None:
            self._banner = check_output(["fish", "--version"]).decode("utf-8")
        return self._banner

    language_info = {
        "name": "fish",
        "codemirror_mode": "shell",
        "mimetype": "text/x-sh",
        "file_extension": ".fish",
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._known_display_ids = set()
        rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
        self.prompt_prefix = f"__FISH_KERNEL_{rand}__> "
        self._start_fish()

    def _start_fish(self):
        old_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_DFL)
        old_sigpipe_handler = signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        try:
            self.fish_session = _FishSession(self.prompt_prefix)
        finally:
            signal.signal(signal.SIGINT, old_sigint_handler)
            signal.signal(signal.SIGPIPE, old_sigpipe_handler)

    def process_output(self, output):
        if not self.silent:
            plain_output, rich_contents = extract_contents(output)

            if plain_output:
                stream_content = {"name": "stdout", "text": plain_output}
                self.send_response(self.iopub_socket, "stream", stream_content)

            for content in rich_contents:
                if isinstance(content, Exception):
                    message = {"name": "stderr", "text": str(content)}
                    self.send_response(self.iopub_socket, "stream", message)
                elif "transient" in content and "display_id" in content["transient"]:
                    self._send_content_to_display_id(content)
                else:
                    self.send_response(self.iopub_socket, "display_data", content)

    def _send_content_to_display_id(self, content):
        """If display_id is unknown, use display_data; otherwise update_display_data."""
        display_id = content["transient"]["display_id"]
        if display_id in self._known_display_ids:
            msg_type = "update_display_data"
        else:
            msg_type = "display_data"
            self._known_display_ids.add(display_id)
        self.send_response(self.iopub_socket, msg_type, content)

    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        self.silent = silent
        if not code.strip():
            return {
                "status": "ok",
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        if code.strip().endswith("\\"):
            error_content = {
                "ename": "",
                "evalue": "Cell has trailing backslash",
                "traceback": [],
            }
            self.send_response(self.iopub_socket, "error", error_content)
            error_content["execution_count"] = self.execution_count
            error_content["status"] = "error"
            return error_content

        interrupted = False
        output = ""
        exitcode = 1
        try:
            output, exitcode = self.fish_session.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.fish_session.child.sendintr()
            interrupted = True
        except EOF:
            output = "Restarting Fish\n"
            self._start_fish()

        if output:
            self.process_output(output)

        if interrupted:
            return {"status": "abort", "execution_count": self.execution_count}

        if exitcode:
            error_content = {"ename": "", "evalue": str(exitcode), "traceback": []}
            self.send_response(self.iopub_socket, "error", error_content)

            error_content["execution_count"] = self.execution_count
            error_content["status"] = "error"
            return error_content

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }

    def do_complete(self, code, cursor_pos):
        code = code[:cursor_pos]
        default = {
            "matches": [],
            "cursor_start": 0,
            "cursor_end": cursor_pos,
            "metadata": {},
            "status": "ok",
        }

        tokens = re.split(r"[\t \n;=\"'><]+", code)
        token = tokens[-1] if tokens else ""
        start = cursor_pos - len(token)

        completion_cmd = "complete --do-complete {} 2>/dev/null".format(
            shlex.quote(code)
        )
        try:
            output, _ = self.fish_session.run_command(completion_cmd, timeout=10)
        except Exception:
            return default

        matches = []
        for line in output.splitlines():
            candidate = line.split("\t", 1)[0].strip()
            if candidate:
                matches.append(candidate)

        if token:
            matches = [m for m in matches if m.startswith(token)]

        if not matches:
            return default

        return {
            "matches": sorted(set(matches)),
            "cursor_start": start,
            "cursor_end": cursor_pos,
            "metadata": {},
            "status": "ok",
        }
