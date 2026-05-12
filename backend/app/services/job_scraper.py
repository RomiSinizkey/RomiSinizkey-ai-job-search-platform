import requests
from backend.app.utils.matcher import calculate_match_score


def fetch_jobs(search: str = "python"):
    url = f"https://remotive.com/api/remote-jobs?search={search}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    jobs = []

    for job in data.get("jobs", [])[:10]:

        combined_text = (
            f"{job.get('title', '')} "
            f"{job.get('category', '')}"
        )

        match_score = calculate_match_score(combined_text)

        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("candidate_required_location"),
            "url": job.get("url"),
            "category": job.get("category"),
            "match_score": match_score,
        })

    jobs.sort(key=lambda job: job["match_score"], reverse=True)
    return jobs