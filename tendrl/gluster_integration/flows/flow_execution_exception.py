class FlowExecutionFailedError(Exception):
    def __init___(self, err):
        self.message = "Flow Execution failed. Error:" + \
                       " %s".format(err)
