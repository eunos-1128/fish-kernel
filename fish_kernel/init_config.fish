# Different platforms have different names for the systemwide fish config
if test -f /etc/fish/config.fish
    source /etc/fish/config.fish
end
if test -f /usr/local/etc/fish/config.fish
    source /usr/local/etc/fish/config.fish
end
if test -f ~/.config/fish/config.fish
    source ~/.config/fish/config.fish
end

# Reset fish_prompt so pexpect can find it
function fish_prompt
    echo "~> "
end

# Unset fish_right_prompt, so that it can't change fish_prompt to something unexpected.
functions --erase fish_right_prompt

# Disable bracketed paste
bind --preset -e enable-bracketed-paste 2>/dev/null; or true
