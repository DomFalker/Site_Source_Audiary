import urllib.request
import urllib.parse
import json
import http.cookiejar

# Create a cookie jar to track cookies
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

BASE_URL = "http://127.0.0.1:8000"

def test_unauthenticated_access():
    print("Testing unauthenticated access to /produtos...")
    # By default, urllib follows redirects, so we disable redirection to check the status code.
    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise urllib.request.HTTPError(req.full_url, code, msg, headers, fp)
            
    no_redirect_opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        no_redirect_opener.open(f"{BASE_URL}/produtos")
        print("FAIL: Accessed /produtos without auth!")
    except urllib.request.HTTPError as e:
        if e.code in [302, 303, 307] and "login" in e.headers.get('Location', ''):
            print(f"SUCCESS: Redirected to /login (Status: {e.code}, Location: {e.headers.get('Location')})")
        else:
            print(f"FAIL: Unexpected status code {e.code} or headers {e.headers}")

def test_invalid_login():
    print("\nTesting invalid login...")
    data = urllib.parse.urlencode({
        "email": "invalid@email.com",
        "password": "wrongpassword"
    }).encode("utf-8")
    
    req = urllib.request.Request(f"{BASE_URL}/users/login", data=data, method="POST")
    try:
        opener.open(req)
        print("FAIL: Invalid login succeeded!")
    except urllib.request.HTTPError as e:
        if e.code == 400:
            error_response = json.loads(e.read().decode("utf-8"))
            print(f"SUCCESS: Got HTTP 400 as expected. Error detail: {error_response.get('detail')}")
        else:
            print(f"FAIL: Expected 400, got {e.code}")

def test_register_and_valid_login():
    print("\nTesting registration, login, and authenticated access...")
    # 1. Register a test user
    reg_data = urllib.parse.urlencode({
        "nome": "Test User",
        "email": "testuser@example.com",
        "senha": "password123",
        "cep": "12345-678",
        "rua": "Test Street",
        "tipo": "buyer"
    }).encode("utf-8")
    
    # We use a custom opener that doesn't fail on redirect (since /register redirects to /login)
    reg_req = urllib.request.Request(f"{BASE_URL}/users/register", data=reg_data, method="POST")
    try:
        response = opener.open(reg_req)
        print("User registration requested successfully.")
    except urllib.request.HTTPError as e:
        # If user already exists, it might raise 400. That's fine for testing.
        if e.code == 400:
            print("User registration: user might already exist (400), continuing...")
        else:
            print(f"Registration failed with code {e.code}")
            return

    # 2. Login with valid credentials
    login_data = urllib.parse.urlencode({
        "email": "testuser@example.com",
        "password": "password123"
    }).encode("utf-8")
    
    login_req = urllib.request.Request(f"{BASE_URL}/users/login", data=login_data, method="POST")
    try:
        login_resp = opener.open(login_req)
        login_result = json.loads(login_resp.read().decode("utf-8"))
        print(f"Login Response: {login_result}")
        
        # Check if cookie was set
        cookies = [cookie.name for cookie in cj]
        print(f"Cookies stored in jar: {cookies}")
        if "access_token" in cookies:
            print("SUCCESS: Cookie access_token found!")
        else:
            print("FAIL: Cookie access_token not found!")
            return
            
        # 3. Access /produtos with the stored cookie
        print("Accessing /produtos with active session cookie...")
        prod_resp = opener.open(f"{BASE_URL}/produtos")
        html_content = prod_resp.read().decode("utf-8")
        if "Olá, <strong" in html_content and "Test User" in html_content:
            print("SUCCESS: Products page loaded and showed personalized 'Olá, Test User' header!")
        else:
            print("FAIL: Personalization not found on page. Content snippet:")
            print(html_content[:300])
            
    except Exception as e:
        print(f"FAIL during login/access flow: {e}")

if __name__ == "__main__":
    test_unauthenticated_access()
    test_invalid_login()
    test_register_and_valid_login()
