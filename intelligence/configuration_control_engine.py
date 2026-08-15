import datetime


class ConfigurationControlEngine:

    def __init__(self):

        print("==============================")
        print("GSIS CONFIGURATION CONTROL ENGINE v1.0 ONLINE")
        print("CENTRAL SYSTEM CONFIGURATION ACTIVE")
        print("==============================")


        self.config = {

            "system_mode":
                "SIMULATION",

            "risk_percent":
                1,

            "max_positions":
                5,

            "minimum_confidence":
                70,

            "minimum_pattern_score":
                60,

            "daily_loss_limit":
                500,

            "execution_enabled":
                True,

            "broker_mode":
                "SIMULATION"

        }



    def get_config(self):


        result = {

            "status":
                "CONFIGURATION LOADED",

            "configuration":
                self.config,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }


        print("==============================")
        print("GSIS CONFIG RESULT")
        print("==============================")
        print(result)


        return result



    def update(
        self,
        key,
        value
    ):

        self.config[key] = value


        return {

            "status":
                "CONFIGURATION UPDATED",

            "key":
                key,

            "value":
                value,

            "timestamp":
                datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()

        }



if __name__ == "__main__":


    engine = ConfigurationControlEngine()


    engine.get_config()
