if [ -z "$PERSONCOMPO_PYTHON_PATH" ]
then
    export PERSONCOMPO_PYTHON_PATH=$PERSONCOMPO_DIR/python/
    export PYTHONPATH=$PERSONCOMPO_PYTHON_PATH:$PYTHONPATH
fi

function personcompo-train-agent-dominoes
{

}