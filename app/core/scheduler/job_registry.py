from app.monitoring.jobs.cucm.ntp_job import CUCMNTPJob

# from app.monitoring.jobs.cucm.show_status_job import (
#     CUCMShowStatusJob
# )


JOB_REGISTRY = {
    "ntp": CUCMNTPJob(),
    # "show_status": CUCMShowStatusJob(),
}