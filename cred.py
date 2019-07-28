source = {
    'client_id': r'3',
    'client_secret': r'0kDzIuhzlW8qHTZJoScEBD2hgdWJTZahBkM1bL2I',
    'url': r'http://arkeyve-firefly.herokuapp.com'
    }
sink = {
    'client_id': r'2',
    'client_secret': r'ewKhUUadfWjBtUuKmRgw4NRY2SpidFBua8Z8KC2Z',
    'url': r'http://localhost/firefly-iii'
    }
source['auth_base_url'] = source['url'] + r'/oauth/authorize'
source['token_url'] = source['url'] + r'/oauth/token'
sink['auth_base_url'] = sink['url'] + r'/oauth/authorize'
sink['token_url'] = sink['url'] + r'/oauth/token'
