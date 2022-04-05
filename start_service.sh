SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
EXEC_SCRIPT="plot_server.py"
PATH_TO_SCRIPT="$SCRIPT_DIR/$EXEC_SCRIPT"
RUN_CMD="python3 $PATH_TO_SCRIPT"

#echo "stopping already running commands: "
#pkill -f $PATH_TO_SCRIPT

echo "running command: $RUN_CMD"
python3 $PATH_TO_SCRIPT > /dev/null 2>&1 &
echo "command started"
exit 0
