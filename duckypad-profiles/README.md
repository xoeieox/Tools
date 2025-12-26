# duckyPad Profile Management

Native workflow for managing duckyPad Pro profiles without the GUI configurator.

## Quick Start

```bash
cd /Users/erhei/Tools/duckypad-profiles

# Edit .txt files directly, then:
make sync    # Compile and push to duckyPad
```

## Commands

| Command | Description |
|---------|-------------|
| `make help` | Show available commands |
| `make compile` | Compile all .txt scripts to .dsb bytecode |
| `make sync` | Compile + push all profiles to duckyPad |
| `make pull` | Pull profiles from duckyPad to local |
| `make status` | Preview what would be synced |
| `make clean` | Remove backup files |

## Workflow

### Editing Profiles

1. **Edit `.txt` files** - Each key script is a plain text duckyScript file
2. **Run `make compile`** - Generates `.dsb` bytecode files
3. **Mount duckyPad** - Hold `+` button, select "Mount USB"
4. **Run `make sync`** - Pushes compiled profiles to device
5. **Eject & unplug** - Always eject before disconnecting

### File Structure

```
duckypad-profiles/
├── Makefile              # Build automation
├── compile.py            # Bytecode compiler
├── profile_info.txt      # Profile index (order and names)
├── profile_General/      # A profile folder
│   ├── config.txt        # Profile config (labels, colors)
│   ├── key1.txt          # Key 1 script (source)
│   ├── key1.dsb          # Key 1 bytecode (compiled)
│   └── ...
└── profile_<AppName>/    # Add more as needed
```

### Adding a New Profile

1. Create folder: `mkdir profile_MyApp`
2. Create `config.txt` with labels and colors
3. Create `keyN.txt` files for each key
4. Add to `profile_info.txt`: `2 MyApp`
5. Run `make sync`

### Profile config.txt Format

```
z1 Label         # Key 1 top label
x1 SubLabel      # Key 1 bottom label (optional)
z2 Key2Label
...
BG_COLOR 64 53 255           # Background RGB
SWCOLOR_1 255 128 0          # Key 1 color RGB
SWCOLOR_21 0 200 100         # Key 21 color RGB
```

### Key Script Format

Scripts use [duckyScript 3](https://docs.hak5.org/hak5-usb-rubber-ducky/) syntax:

```ducky
REM This is a comment
STRING Hello World        # Type text
ENTER                     # Press Enter
GUI SPACE                 # Cmd+Space (Spotlight on macOS)
DELAY 500                 # Wait 500ms
MK_VOLUP                  # Media key: volume up
NEXT_PROFILE              # Switch to next profile
PREV_PROFILE              # Switch to previous profile
```

#### Common Commands

| Command | Description |
|---------|-------------|
| `STRING text` | Type text |
| `STRINGLN text` | Type text + Enter |
| `ENTER`, `TAB`, `ESCAPE` | Press key |
| `GUI key` | Cmd+key (macOS) / Win+key |
| `CTRL key`, `ALT key`, `SHIFT key` | Modifier combos |
| `DELAY ms` | Wait milliseconds |
| `MK_VOLUP`, `MK_VOLDOWN`, `MK_MUTE` | Media keys |
| `MK_PLAY`, `MK_NEXT`, `MK_PREV` | Playback controls |
| `NEXT_PROFILE`, `PREV_PROFILE` | Profile navigation |
| `GOTO_PROFILE n` | Jump to profile number |

#### OLED Display

```ducky
OLED_CLEAR
OLED_CURSOR 10 50         # x, y position
OLED_PRINT Hello World
OLED_UPDATE
```

#### Variables and Logic

```ducky
VAR $count = 0
WHILE $count < 5
    STRING Hello
    ENTER
    $count = $count + 1
END_WHILE
```

## Related Tools

All tools are in `/Users/erhei/Tools/`:

### Configurator (GUI)

```bash
cd /Users/erhei/Tools/duckyPad-Configurator
sudo .venv/bin/python3 src/duckypad_config.py
```

### Autoswitcher (Background Daemon)

Automatically switches profiles based on active application.

```bash
# Check if running
sudo launchctl list | grep duckypad

# View logs
tail -f /Users/erhei/Tools/duckypad_autoswitcher.log
tail -f /Users/erhei/Tools/duckypad_autoswitcher.error.log

# Restart daemon
sudo launchctl unload /Library/LaunchDaemons/com.duckypad.autoswitcher.plist
sudo launchctl load /Library/LaunchDaemons/com.duckypad.autoswitcher.plist
```

App-to-profile mappings are configured through the Configurator GUI.

### Dependencies

- `../duckyPad-Configurator/` - Configurator source + bytecode compiler
- `../duckyPad-profile-autoswitcher/` - Autoswitcher source

## Resources

- [duckyPad Pro Documentation](https://dekunukem.github.io/duckyPad-Pro/)
- [duckyScript Reference](https://dekunukem.github.io/duckyPad-Pro/doc/duckyscript_info.html)
- [duckyPad Discord](https://discord.gg/4sJCBx5)
