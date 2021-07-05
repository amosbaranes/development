class VirtualHostMiddleware:
    virtual_hosts = {
        "www.drbaranes.com": "academycity.drbaranes_com_urls",
        "drbaranes.com": "academycity.drbaranes_com_urls",
        "www.ugandatowns.com": "academycity.ugandatowns_com_urls",
        "*.ugandatowns.com": "academycity.ugandatowns_com_urls",
        "ugandatowns.com": "academycity.ugandatowns_com_urls",
        "academycity.org": "academycity.urls",
        "www.academycity.org": "academycity.urls",
        "127.0.0.1:8000": "academycity.urls",
        "127.0.0.1:8001": "academycity.urls",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # let's configure the root urlconf
        host = request.get_host().lower()
        # print(host)
        # print(self.virtual_hosts.get(host))
        request.urlconf = self.virtual_hosts.get(host)
        # order matters!
        response = self.get_response(request)
        return response

