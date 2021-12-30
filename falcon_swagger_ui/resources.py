import json
from . import StaticAsyncSinkAdapter, StaticSyncSinkAdapter, SwaggerUiSyncResource, SwaggerUiAsyncResource


def register_swaggerui_app(app, swagger_uri, api_url, page_title='Swagger UI', favicon_url=None, config=None, uri_prefix="", is_async=False):

    """:type app: falcon.API"""

    templates_folder = 'templates'
    static_folder = 'dist'

    default_config = {
        'client_realm': 'null',
        'client_id': 'null',
        'client_secret': 'null',
        'app_name': 'null',
        'docExpansion': "none",
        'jsonEditor': False,
        'defaultModelRendering': 'schema',
        'showRequestHeaders': False,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch'],
    }

    if config:
        default_config.update(config)

    default_context = {
        'page_title': page_title,
        'favicon_url': favicon_url,
        'base_url': uri_prefix + swagger_uri,
        'api_url': api_url,
        'app_name': default_config.pop('app_name'),
        'client_realm': default_config.pop('client_realm'),
        'client_id': default_config.pop('client_id'),
        'client_secret': default_config.pop('client_secret'),
        # Rest are just serialized into json string
        # for inclusion in the .js file
        'config_json': json.dumps(default_config)
    }

    if is_async:
        class_skin_name = StaticAsyncSinkAdapter
        class_swagger_ui_name = SwaggerUiAsyncResource
    else:
        class_skin_name = StaticSyncSinkAdapter
        class_swagger_ui_name = SwaggerUiSyncResource

    if  swagger_uri.endswith('/'):
        app.add_sink(
            class_skin_name(static_folder),
            r'%s(?P<filepath>.*)\Z' % swagger_uri,
        )
    else:
        app.add_sink(
            class_skin_name(static_folder),
            r'%s/(?P<filepath>.*)\Z' % swagger_uri,
        )

    if swagger_uri == '/':
        default_context['base_url'] = uri_prefix

    app.add_route(
        swagger_uri,
        class_swagger_ui_name(templates_folder, default_context)
    )
