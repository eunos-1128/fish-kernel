# Keep startup deterministic for pexpect.
set -g fish_greeting

set -l fish_kernel_prompt "__FISH_KERNEL_PROMPT__> "
if set -q FISH_KERNEL_PROMPT
    set fish_kernel_prompt $FISH_KERNEL_PROMPT
end

function fish_prompt --description "fish-kernel startup prompt"
    printf "%s" "$fish_kernel_prompt"
end

function fish_right_prompt --description "Disable right prompt in fish-kernel"
end

function fish_mode_prompt --description "Disable mode prompt in fish-kernel"
end
