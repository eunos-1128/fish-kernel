import fish_kernel.display as display
import fish_kernel.kernel as kernel


def test_split_lines_handles_mixed_line_endings():
    text = "a\r\nb\nc\rd"

    assert display.split_lines(text) == ["a\n", "b\n", "c\r", "d\n"]


def test_filename_and_display_id_parsing():
    assert display._filename_and_display_id("/tmp/file.txt") == ("/tmp/file.txt", None)
    assert display._filename_and_display_id("(plot1) /tmp/file.txt") == (
        "/tmp/file.txt",
        "plot1",
    )
    assert display._filename_and_display_id("(plot1)/tmp/file.txt") == (
        "/tmp/file.txt",
        "plot1",
    )


def test_extract_contents_separates_plain_and_rich(monkeypatch):
    prefix = "fish_kernel: saved custom data to: "

    def fake_display_data(filename):
        return {"data": {"text/plain": filename}, "metadata": {}}

    monkeypatch.setattr(
        display,
        "CONTENT_DATA_PREFIXES",
        {
            prefix: {
                "display_cmd": "displayCustom",
                "display_data_fn": fake_display_data,
                "capability": "custom",
            }
        },
    )

    output = f"first line\n{prefix}(chart-1) /tmp/rich.txt\nsecond line\n"
    plain_output, rich_contents = display.extract_contents(output)

    assert plain_output == "first line\nsecond line\n"
    assert rich_contents == [
        {
            "data": {"text/plain": "/tmp/rich.txt"},
            "metadata": {},
            "transient": {"display_id": "chart-1"},
        }
    ]


def test_strip_control_sequences_removes_terminal_escapes():
    text = "A\x1b[31mB\x1b[0mC\x1b]0;title\x07D\x1bPfoo\x1b\\E\x1bX"

    assert kernel._strip_control_sequences(text) == "ABCDE"
