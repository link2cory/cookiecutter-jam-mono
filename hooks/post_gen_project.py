import os, subprocess

# cookiecutter jinja2 obj is extracted as an OrderedDict
from collections import OrderedDict
from cookiecutter.main import cookiecutter
from github import Github
from git import Repo

# extract the context from the cookiecutter jinja2 obj
# it is much easier to work with this way...
context = {{ cookiecutter }}

# run cookiecutter for each sub-package
for name, package in context['packages'].items():
    # make sure that the dependencies for this package don't get installed yet
    package_context = package['context']
    package_context['is_subpackage'] = True
    
    success = cookiecutter(
        package['template'],
        output_dir='packages',
        extra_context=package_context,
        no_input=True
    )

if context['is_subpackage'] == 'no':
    if context['install_dependencies'] == 'yes':
        subprocess.run(['yarn', 'install'])

    if context['use_git'] == 'yes':
        # activate .gitignore. It must be stored this way to facilitate versioning of
        # the cookiecutter.
        os.rename('gitignore', '.gitignore')

        # initialize local repo
        local_repo = Repo.init(os.getcwd())
        local_repo.git.add(A=True)
        local_repo.index.commit('Initial Commit, project generated with cookiecutter-jam-app')

        if context['use_github'] == 'yes':
            # create the github repo
            Github('{{ cookiecutter.github_token }}').get_user().create_repo('{{ cookiecutter.project_slug }}')
            # point local repo to the remote
            remote_repo = local_repo.create_remote(
                'origin',
                'git@github.com:{{ cookiecutter.github_user }}/{{ cookiecutter.project_slug }}.git'
            )
            #  push to the remote
            remote_repo.push(refspec='{}:{}'.format('master', 'master'))

    # Remove github actions files unless they are necessary
    if context['use_github'] == 'no' || context['continuous_integration'] != 'github_actions':
        # remove the github directory
        os.rmtree('.github/')
