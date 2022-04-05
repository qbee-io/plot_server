SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
EXEC_SCRIPT="plot_server.py"
PATH_TO_SCRIPT="$SCRIPT_DIR/$EXEC_SCRIPT"

echo "stopping already running commands with $PATH_TO_SCRIPT"
pkill -f $PATH_TO_SCRIPT

exit 0
