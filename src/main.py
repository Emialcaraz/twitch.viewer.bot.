from settings import EnvironmentTypeEnum, settings
from dv_twitch_viewer.logger import configure_logger
from dv_twitch_viewer.orchestrator import Orchestrator
import logging

def main():
    configure_logger()
    orch = Orchestrator()
    orch.start()

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    try:
        orch.run()
    except Exception as exc:
        print(exc)
        if settings.ENV_TYPE == EnvironmentTypeEnum.development:
            raise exc
    finally:
        orch.stop()


if __name__ == "__main__":
    main()
