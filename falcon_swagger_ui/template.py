import os
import jinja2


class TemplateBase(object):

    def __init__(self, templates_path):
        self.tpl_path = templates_path
    
    def _load_template(self, tpl, enable_async=False):

        curr_dir = os.path.dirname(os.path.abspath(__file__))

        path, filename = os.path.split(tpl)

        templates_directory = os.path.join(curr_dir, self.tpl_path)

        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(path, templates_directory)
            ),
            enable_async=enable_async
        ).get_template(filename)


class TemplateSyncRenderer(TemplateBase):

    def render(self, tpl_name, *args, **kwargs):
        template = self._load_template(tpl_name)
        return template.render(*args, **kwargs)


class TemplateAsyncRenderer(TemplateBase):

    async def render(self, tpl_name, *args, **kwargs):
        template = self._load_template(tpl_name, enable_async=True)
        return await template.render_async(*args, **kwargs)