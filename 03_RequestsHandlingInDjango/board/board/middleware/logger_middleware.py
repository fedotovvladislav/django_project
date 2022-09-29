from datetime import datetime


class LoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        method = request.META.get('REQUEST_METHOD')
        url_request = request.META.get('HTTP_HOST')
        path_request = request.META.get('PATH_INFO')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('logs.log', 'a') as logs:
            logs.write(f'ip: {ip}\t\tMethod: {method}\t\tURL: {url_request}{path_request}\t\tTime: {time}\n')
        response = self.get_response(request)

        return response
