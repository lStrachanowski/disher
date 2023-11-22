class  GlobalValues:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Dynamically set the global value based on some condition
        
        request.global_value = 'ee'
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        print(request.global_value)
        
        return response
        