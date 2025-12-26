# duckyPad Profile Sync
# Syncs local profiles to the duckyPad SD card

# Change this to match your duckyPad volume name
DUCKYPAD_VOLUME := /Volumes/DP24_CD90

# Profiles to sync (all profile_* folders)
PROFILES := $(wildcard profile_*)

# Python from configurator venv
PYTHON := ../duckyPad-Configurator/.venv/bin/python3

.PHONY: sync pull status clean help compile

help:
	@echo "duckyPad Profile Management"
	@echo ""
	@echo "  make compile - Compile .txt scripts to .dsb bytecode"
	@echo "  make sync    - Compile and push profiles to duckyPad"
	@echo "  make pull    - Pull profiles from duckyPad to local"
	@echo "  make status  - Show what would change"
	@echo "  make clean   - Remove backup files"
	@echo ""
	@echo "Volume: $(DUCKYPAD_VOLUME)"
	@echo "Profiles: $(PROFILES)"

compile:
	@$(PYTHON) compile.py

sync: compile
	@if [ ! -d "$(DUCKYPAD_VOLUME)" ]; then \
		echo "Error: duckyPad not mounted at $(DUCKYPAD_VOLUME)"; \
		echo "Hold + button on duckyPad and select 'Mount USB'"; \
		exit 1; \
	fi
	@echo "Syncing profiles to duckyPad..."
	@for profile in $(PROFILES); do \
		echo "  → $$profile"; \
		rsync -av --delete "$$profile/" "$(DUCKYPAD_VOLUME)/$$profile/"; \
	done
	@if [ -f "dp_settings.txt" ]; then \
		echo "  → dp_settings.txt"; \
		cp dp_settings.txt "$(DUCKYPAD_VOLUME)/"; \
	fi
	@if [ -f "profile_info.txt" ]; then \
		echo "  → profile_info.txt"; \
		cp profile_info.txt "$(DUCKYPAD_VOLUME)/"; \
	fi
	@echo "Done! Eject duckyPad before unplugging."

pull:
	@if [ ! -d "$(DUCKYPAD_VOLUME)" ]; then \
		echo "Error: duckyPad not mounted at $(DUCKYPAD_VOLUME)"; \
		exit 1; \
	fi
	@echo "Pulling profiles from duckyPad..."
	@for profile in "$(DUCKYPAD_VOLUME)"/profile_*/; do \
		name=$$(basename "$$profile"); \
		echo "  ← $$name"; \
		rsync -av "$$profile/" "./$$name/"; \
	done
	@if [ -f "$(DUCKYPAD_VOLUME)/dp_settings.txt" ]; then \
		echo "  ← dp_settings.txt"; \
		cp "$(DUCKYPAD_VOLUME)/dp_settings.txt" .; \
	fi
	@echo "Done!"

status:
	@if [ ! -d "$(DUCKYPAD_VOLUME)" ]; then \
		echo "Error: duckyPad not mounted at $(DUCKYPAD_VOLUME)"; \
		exit 1; \
	fi
	@echo "Changes that would sync:"
	@for profile in $(PROFILES); do \
		rsync -avn --delete "$$profile/" "$(DUCKYPAD_VOLUME)/$$profile/" | grep -v "^$$" || true; \
	done

clean:
	find . -name "*.bak" -delete
	find . -name "*~" -delete
