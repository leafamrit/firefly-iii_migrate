source = {
    'client_id': r'<source_client_id>',
    'client_secret': r'<source_client_secret>',
    'url': r'<source_url>'
    }
sink = {
    'client_id': r'<sink_client_id>',
    'client_secret': r'<sink_client_secret>',
    'url': r'<sink_url>'
    }
source['auth_base_url'] = source['url'] + r'/oauth/authorize'
source['token_url'] = source['url'] + r'/oauth/token'
sink['auth_base_url'] = sink['url'] + r'/oauth/authorize'
sink['token_url'] = sink['url'] + r'/oauth/token'
