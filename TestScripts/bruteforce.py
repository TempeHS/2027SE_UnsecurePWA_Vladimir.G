import time
import requests

url = "http://127.0.0.1:5000/"

usernames = ["test_student1", "test_no_user1", "test_admin1"]
passwords = ["wrong_password1", "wrong_passwords2", "secret"]

for username in usernames:
    for password in passwords:
        response = requests.post(
            url,
            data={"username": username, "password": password},
            timeout=10,
            allow_redirects=False,
        )

        response.raise_for_status()

        if response.status_code != 200:
            raise RuntimeError(f"Unexpected response: {response.status_code} ")

        success_marker = f"<h1>Welcome {username}!</h1>"

        if success_marker in response.text:
            print(f"Login accepted: {username} / {password}")
        elif "<h1>Login</h1>" in response.text:
            print(f"Login rejected: {username} / {password}")
        else:
            raise RuntimeError("Unrecognised page; check the response")

        time.sleep(1)
