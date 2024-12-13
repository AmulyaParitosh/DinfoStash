import asyncio

from dinfostash.agent.constants import TailorSection, experience_agent, project_agent
from dinfostash.data.models import ResumeData


async def tailor_resume(resume: ResumeData, job_description: str) -> ResumeData:

    project_task = project_agent.run(
        job_description, deps=TailorSection("Project", resume.projects)
    )

    exp_task = experience_agent.run(
        job_description, deps=TailorSection("Experience", resume.experience)
    )

    project_resp, exp_resp = await asyncio.gather(project_task, exp_task)

    resume.projects = project_resp.data
    resume.experience = exp_resp.data

    return resume


if __name__ == "__main__":
    import json

    with open(
        "/home/encryptedbee/Documents/Resumes/Amulya/data/amulya_resume_data_complete.json"
    ) as f:
        resume = ResumeData(**json.load(f))
    with open(
        "/home/encryptedbee/Projects/Dinfo/DinfoStash/.dev_utils/job_description.txt"
    ) as f:
        job_desc = f.read()

    new_resume = asyncio.run(tailor_resume(resume, job_desc))
    print(new_resume.model_dump_json(indent=4))
    with open(
        "/home/encryptedbee/Projects/Dinfo/DinfoStash/.dev_utils/ai_resume.json", "w"
    ) as f:
        json.dump(new_resume.model_dump(), f, indent=4)
