import os, subprocess

from cookiecutter.main import cookiecutter
from github import Github
from git import Repo

# run cookiecutter for each sub-package
for name, package in {{ cookiecutter.packages | dictsort }}:
    # make sure that the dependencies for this package don't get installed yet
    context = package['context']
    context['is_subpackage'] = True

    success = cookiecutter(
        package['template'],
        output_dir='packages',
        extra_context=context,
        no_input=True
    )

{% if cookiecutter.is_subpackage == 'no' -%}
    {% if cookiecutter.install_dependencies == 'yes' -%}
        subprocess.run(['yarn', 'install'])
    {% endif %}

    {% if cookiecutter.use_git == 'yes' -%}
        # initialize local repo 
        local_repo = Repo.init(os.getcwd())
        local_repo.git.add(A=True)
        local_repo.index.commit('Initial Commit, project generated with cookiecutter-jam-app')

        {% if cookiecutter.use_github == 'yes' -%}
            # create the github repo
            Github('{{ cookiecutter.github_token }}').get_user().create_repo('{{ cookiecutter.project_slug }}')
            # point local repo to the remote
            remote_repo = local_repo.create_remote(
                'origin',
                'git@github.com:{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}.git'
            )
            #  push to the remote
            remote_repo.push(refspec='{}:{}'.format('master', 'master'))
        {% endif %}
    {% endif %}
{% endif %}
