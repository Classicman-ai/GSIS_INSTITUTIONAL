from datetime import datetime, timezone


class GSISContextSync:

    def __init__(self, context):
        self.context = context


    def sync(self, engine_name, result):

        if result is None:
            return

        # Convert engine name to context attribute
        name = engine_name.lower()

        # Store engine output dynamically
        setattr(
            self.context,
            name,
            result
        )


        return {
            "engine": "GSIS CONTEXT SYNCHRONIZER",
            "version": "1.0",
            "updated_engine": engine_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "CONTEXT_UPDATED"
        }



def update_context(context, engine_name, result):

    syncer = GSISContextSync(context)

    return syncer.sync(
        engine_name,
        result
    )


if __name__ == "__main__":

    print("GSIS CONTEXT SYNCHRONIZER v1.0 READY")
