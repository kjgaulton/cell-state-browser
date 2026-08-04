#!/bin/zsh
cd "$(dirname "$0")"
echo "Starting Cell State Model Editor..."
export TK_SILENCE_DEPRECATION=1

# Apple's system python3 links against an old, buggy Tcl/Tk 8.5 that fails to
# draw Label/Entry/Text/Listbox widgets on modern macOS (buttons still look
# fine, which is the telltale sign). Prefer a Homebrew python3, which bundles
# a modern Tcl/Tk, if one is installed.
PYTHON_BIN="python3"
for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3; do
  if [[ -x "$candidate" ]]; then
    PYTHON_BIN="$candidate"
    break
  fi
done
echo "Using interpreter: $PYTHON_BIN"

"$PYTHON_BIN" -u cell_state_simple_app.py
exit_code=$?
echo
if [[ $exit_code -eq 0 ]]; then
  echo "Cell State Model Editor closed."
else
  echo "The app exited with status $exit_code."
fi
echo "Log file: $(pwd)/cell_state_app.log"
echo "Press Return to close this window."
read
