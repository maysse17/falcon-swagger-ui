from . import TemplateAsyncRenderer, TemplateSyncRenderer


class SwaggerUiSyncResource(object):

    def __init__(self, templates_folder, default_context):
        self.templates = TemplateSyncRenderer(templates_folder)
        self.context = default_context

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        resp.text = self.templates.render('index.html', **self.context)


class SwaggerUiAsyncResource(SwaggerUiSyncResource):

    def __init__(self, templates_folder, default_context):
        self.templates = TemplateAsyncRenderer(templates_folder)
        self.context = default_context

    async def on_get(self, req, resp):
        resp.content_type = 'text/html'
        resp.text = await self.templates.render('index.html', **self.context)