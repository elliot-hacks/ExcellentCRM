import requests
import time
from django.core.cache import cache


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
    """Fetch location information with rate limit handling."""
    cache_key = f"ip_location_{ip_address}"  # ✅ Cache key for this IP
    cached_location = cache.get(cache_key)  # ✅ Check if data exists in cache

    if cached_location:
        return cached_location  # ✅ Use cached data

    try:
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()

        if 'error' in response and response.get('reason') == "RateLimited":
            print("🚨 Warning: Rate-limited. Using fallback data.")
            return {}  # ✅ Return empty dict to avoid breaking code

        location_data = {
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name"),
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude"),
            "timezone": response.get("timezone"),
            "isp": response.get("org"),
        }

        cache.set(cache_key, location_data, timeout=86400)  # ✅ Cache for 24 hours
        return location_data

    except Exception as e:
        print(f"🚨 Failed to fetch IP location: {e}")
        return {}