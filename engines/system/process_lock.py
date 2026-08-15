import os
import sys
import time
import fcntl
from datetime import datetime, timezone


LOCK_FILE = os.path.expanduser(
    "~/GSIS/data/system/gsis_daemon.lock"
)


class ProcessLock:

    def __init__(self):
        self.lock = None


    def acquire(self):

        os.makedirs(
            os.path.dirname(LOCK_FILE),
            exist_ok=True
        )

        self.lock = open(
            LOCK_FILE,
            "w"
        )

        try:

            fcntl.flock(
                self.lock,
                fcntl.LOCK_EX | fcntl.LOCK_NB
            )

            self.lock.write(
                str(os.getpid())
            )

            self.lock.flush()

            return True


        except BlockingIOError:

            return False



    def release(self):

        if self.lock:

            try:
                fcntl.flock(
                    self.lock,
                    fcntl.LOCK_UN
                )

                self.lock.close()

            except:

                pass



def check_lock():

    lock = ProcessLock()

    if not lock.acquire():

        print("==============================")
        print("GSIS PROCESS LOCK")
        print("==============================")
        print("ANOTHER GSIS DAEMON IS RUNNING")
        print("START BLOCKED")
        print("==============================")

        sys.exit(1)


    print("==============================")
    print("GSIS PROCESS LOCK ACTIVE")
    print("==============================")
    print(
        {
            "status": "LOCKED",
            "pid": os.getpid(),
            "timestamp":
            datetime.now(
                timezone.utc
            ).isoformat()
        }
    )

    return lock



if __name__ == "__main__":

    lock = check_lock()

    while True:
        time.sleep(60)
