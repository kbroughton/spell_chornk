# python_template_repo

Created via "Use this template" button from template_repo

This is the python class of template repos. More child repos could include jupyter_notebook or flask.

Experimental:
We used templating instead of forking to create this child repo without knowing if it will allow us to merge in specially tagged commits back into the parent template_repo.

Todo:

* Jupyter notebook support (possibly child template repo)
** pip install nbdime
** pip install nbstripout


--------------------------------------------------------------------------------------------------
## parent repo: template_repo

We assume for now that for minimum deployment utility we will need Docker and expect the following
Dockerfiles 
* Dockerfile - (dev.Dockerfile)
* prod.Dockerfile - hardened but still useful 
* sec.Dockerfile - experimental and sometimes prohibitively hardened
* test.Dockerfile - staging/test gate accepting updates from sec. or dev. Dockerfiles


The archetype template child will be python_template_repo which will include package versioning (pip), setup.py, python linting, security checks for dependencies etc. If during the course of development we introduce a convention in template_repo_python which is not specific to python, we can merge that commit back into template_repo.

It's interesting to consider licensing since GitHub requires it to set up a repo. It seems natural to pick the least restrictive license (MIT) and child repos (forks) can only become more restrictive (GPLV3). 
