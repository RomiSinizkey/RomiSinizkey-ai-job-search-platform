sent_jobs = set()


def send_new_jobs_notification(jobs: list[dict]):

    new_jobs = []

    for job in jobs:

        if job["url"] in sent_jobs:
            continue

        sent_jobs.add(job["url"])
        new_jobs.append(job)

    if not new_jobs:
        return

    print("\nNEW JOBS FOUND\n")

    for job in new_jobs:
        print(
            f"{job['title']} | "
            f"{job['company']} | "
            f"Score: {job['match_score']}"
        )

    print()