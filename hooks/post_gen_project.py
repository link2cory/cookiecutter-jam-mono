import subprocess 

from cookiecutter.main import cookiecutter

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
