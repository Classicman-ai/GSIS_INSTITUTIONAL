import subprocess
import time
import os
import signal


print("==============================")
print("GSIS MASTER LAUNCHER v1.0")
print("==============================")


ENGINES = [

    "engines.data.market_bridge",

    "engines.scoring.regime_score_engine",

    "engines.bayesian.bayesian_engine",

    "engines.signal.master_signal_engine",

    "engines.confirmation.confirmation_engine",

    "engines.qualification.qualification_engine",

    "engines.risk.risk_engine",

    "engines.execution.execution_engine",

    "engines.trade_manager.trade_manager",

    "engines.alert.telegram_engine",

    "engines.telegram.command_center"

]


processes=[]



def start_engine(module):

    try:

        p=subprocess.Popen(
            [
                "python",
                "-m",
                module
            ]
        )

        processes.append(
            {
                "module":module,
                "pid":p.pid,
                "process":p
            }
        )

        print(
            "STARTED:",
            module,
            "PID:",
            p.pid
        )


    except Exception as e:

        print(
            "FAILED:",
            module,
            e
        )



def shutdown(sig,frame):

    print("\nGSIS SHUTDOWN")

    for p in processes:

        try:
            os.kill(
                p["pid"],
                signal.SIGTERM
            )

        except:
            pass


    exit()



signal.signal(
    signal.SIGINT,
    shutdown
)



def run():

    for engine in ENGINES:

        start_engine(engine)

        time.sleep(1)


    print("==============================")
    print("GSIS ALL SYSTEMS ONLINE")
    print("==============================")


    while True:


        for item in processes:

            if item["process"].poll() is not None:

                print(
                    "RESTARTING:",
                    item["module"]
                )

                item["process"]=subprocess.Popen(
                    [
                    "python",
                    "-m",
                    item["module"]
                    ]
                )

                item["pid"]=item["process"].pid



        time.sleep(10)



if __name__=="__main__":

    run()
