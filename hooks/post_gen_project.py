import os, subprocess

from cookiecutter.main import cookiecutter
from git import Repo

# run cookiecutter for each sub-package
for name, package in {{ cookiecutter.packages | dictsort }}:
    # make sure that the dependencies for this package don't get installed yet
    context = package['context']
    context['install_dependencies'] = False

    success = cookiecutter(
        package['template'],
        output_dir='packages',
        extra_context=context,
        no_input=True
    )

# install dependencies
{% if cookiecutter.install_dependencies == 'yes' -%}
    subprocess.run(['yarn', 'install'])
{% endif %}


{% if cookiecutter.is_subproject == 'no' and cookiecutter.use_git == 'yes' -%}
    # initialize local repo 
    local_repo = Repo.init(os.getcwd())
    local_repo.git.add(A=True)
    local_repo.index.commit('Initial Commit, project generated with cookiecutter-jam-app')
{% endif %}
