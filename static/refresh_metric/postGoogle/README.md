# Post a text on Google+
Program can provide a way to publish text on Google+ using selenium.

## How use it

Run `python getCookies.py` and log in with the account that you want publish, and press `Enter` button. It will
generate `cookies.pkl` file with your cookies.

Once you have a `cookies.pkl` file, execute `python post.py ["text"]`. If text is empty, a default text will be published.
