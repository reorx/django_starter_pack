import jinja2
from jinja2 import PackageLoader
from django.utils.timezone import template_localtime
from django.http import HttpResponse
from django.views.generic import View


root_pkg_name = 'starter_app'
template_dir_name = 'templates'


def get_jinja2_env():
    loader = PackageLoader(root_pkg_name, package_path=template_dir_name)
    env = jinja2.Environment(loader=loader)
    env.filters.update({
        'localtime': template_localtime,
    })
    env.globals.update({
        'localtime': template_localtime,
    })
    # env.filters['round_str'] = round_str
    return env


jinja2_env = get_jinja2_env()


def get_template(name):
    return jinja2_env.get_template(name)


# jinja2 equivant of django.shortcuts.render
def render(request, template_name, context: dict, status=200):
    return HttpResponse(
        get_template(template_name).render(**context),
        status=status,
    )


class WebView(View):
    template_name = ''

    def render_to_response(self, template_name=None, context=None, status=200):
        if context is None:
            context = {}
        if not template_name:
            template_name = self.template_name

        # add functions here
        # context.update(
        #     foo=foo,
        # )
        return render(
            self.request,
            template_name,
            context,
            status=status,
        )
