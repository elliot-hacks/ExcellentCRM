import requests

def get_ip(request):
    """Retrive IP addresses from api"""
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]
    """Retrieve the IP address from the request headers."""
    # x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(",")[0]  # Get the first IP in the list
    # else:
    #     ip = request.META.get("REMOTE_ADDR")  # Get the remote address
    # return ip

def get_location(ip_address):
    """Fetch location information for a given IP address using ipapi API."""
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    
    # ✅ Exclude "ip" key (which caused FieldError)
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
        "timezone": response.get("timezone"),  # ✅ Added timezone
        "isp": response.get("org"),  # ✅ Added ISP field
    }

    return location_data  # ✅ Returns valid fields
