import subprocess
import os
import fcntl
import select

class Terminal:
    def __init__(self):
        self.process = subprocess.Popen(
            ["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
        )
        # Make the stdout and stderr non-blocking
        fl = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        fl = fcntl.fcntl(self.process.stderr, fcntl.F_GETFL)
        fcntl.fcntl(self.process.stderr, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        self.history = []

    def run_command(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

        output, error = self._read_output()
        self.history.append((command, output, error))
        return output, error

    def _read_output(self):
        output, error = "", ""
        while True:
            readx = select.select([self.process.stdout, self.process.stderr], [], [], 0.1)[0]
            for output_stream in readx:
                if output_stream == self.process.stdout:
                    output_line = self.process.stdout.read()
                    if output_line:
                        output += output_line
                elif output_stream == self.process.stderr:
                    error_line = self.process.stderr.read()
                    if error_line:
                        error += error_line
            if not readx:
                break
        return output, error
    

    def return_history_as_dict(self):
        """
        Returns the history of commands and their outputs as a list of dictionaries.
        """
        history_list = []
        for i, (command, output, error) in enumerate(self.history, 1):
            history_list.append({
                'id': i,
                'command': command,
                'output': output,
                'error': error
            })
        return history_list

    def close(self):
        self.process.terminate()