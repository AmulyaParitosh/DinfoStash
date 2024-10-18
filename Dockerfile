FROM python:3.11-slim

LABEL key=org.opencontainers.image.source value="https://github.com/AmulyaParitosh/ResumeGenerator"
LABEL key=org.opencontainers.image.description value="ResumeGenerator is an API that generates a resume in pdf format using the data provided in a json file."
LABEL key=org.opencontainers.image.licenses value="MIT"

# RUN apt-get update && apt=get install texlive-full
RUN apt-get -y update
RUN apt-get -y install --fix-missing sudo texlive-full
RUN rm -rf /var/lib/apt/lists/*


# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false

# copying configuration files and installing dependencies to new directory- /project
COPY pyproject.toml pdm.lock README.md firebase.json .env /project/

WORKDIR /project

RUN pdm install --check --prod --no-editable

# copying source code to /project/src
COPY src /project/src

CMD ["uvicorn", "src.dinfostash:app", "--host", "0.0.0.0", "--port", "80"]
