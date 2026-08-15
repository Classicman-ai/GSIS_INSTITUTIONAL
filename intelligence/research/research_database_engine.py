import os
import json
import datetime


class ResearchDatabaseEngine:

    def __init__(self):

        print("==============================")
        print("GSIS RESEARCH DATABASE ENGINE v1.0 ONLINE")
        print("INSTITUTIONAL KNOWLEDGE DATABASE ACTIVE")
        print("==============================")

        self.base_path = "database"

        self.directories = [

            "market_data",
            "economic_events",
            "market_reactions",
            "signals",
            "trades",
            "learning",
            "analytics",
            "logs"

        ]

        self.initialize_database()


    def initialize_database(self):

        os.makedirs(self.base_path, exist_ok=True)

        for folder in self.directories:

            os.makedirs(

                os.path.join(
                    self.base_path,
                    folder
                ),

                exist_ok=True

            )


    def save_record(

        self,
        category,
        filename,
        data

    ):

        path = os.path.join(

            self.base_path,

            category,

            filename

        )


        with open(path, "w") as f:

            json.dump(

                data,

                f,

                indent=4

            )


        return path


    def load_record(

        self,
        category,
        filename

    ):

        path = os.path.join(

            self.base_path,

            category,

            filename

        )


        if not os.path.exists(path):

            return None


        with open(path, "r") as f:

            return json.load(f)


    def database_status(self):

        summary = {}

        for folder in self.directories:

            location = os.path.join(

                self.base_path,

                folder

            )

            summary[folder] = len(

                os.listdir(location)

            )


        result = {

            "status":

                "DATABASE READY",

            "folders":

                summary,

            "timestamp":

                datetime.datetime.now(

                    datetime.timezone.utc

                ).isoformat()

        }


        print("==============================")
        print("GSIS DATABASE STATUS")
        print("==============================")
        print(result)

        return result



if __name__ == "__main__":

    engine = ResearchDatabaseEngine()


    sample = {

        "event":

            "SYSTEM INITIALIZATION",

        "message":

            "GSIS DATABASE CREATED"

    }


    engine.save_record(

        "logs",

        "startup.json",

        sample

    )


    engine.database_status()
