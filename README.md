The authorization process requires valid client credentials: a client ID and a client secret. You can follow the Apps guide to learn how to generate them.

We're using PKCE autohorization

1. Generates a high-entropy code verifier
2. Hashes it with SHA-256
3. Encodes it using base64url (no padding) to produce the code challenge

a. new URLSearchParams(params) → urllib.parse.urlencode(params)
In Python, the urlencode() function takes a dictionary and converts it into a URL-safe query string, handling special characters and spaces (like those in your scope string) automatically.
b. authUrl.toString() → String Formatting (f"{base}?{query}")
While JavaScript's URL object manages the ? and separators for you, in Python you typically join the base URL and the encoded query string manually using an f-string or +.
c. window.location.href → return redirect(url)
In a Flask route, returning a redirect() object instructs the user's browser to navigate to the new address.

If you have 30 friends, you’ve hit the "Developer's Wall."

As of late 2025, Spotify has made it significantly harder for individual developers to scale up. If you try to add that 26th friend, you’ll run into a hard limit. Here is the reality of the situation:

### 1. The 25-User Hard Limit

In **Development Mode**, Spotify allows exactly **25 unique Spotify accounts** to be "allowlisted."

- **Manual Entry:** You have to manually type in the email address (the one linked to their Spotify account) for every single friend in the Developer Dashboard.
- **The 26th Friend:** If someone not on your list tries to log in, your app will receive a `403 Forbidden` error from the API.

### 2. The "Extended Quota" Trap

Previously, you could just apply for an extension. Now, the rules are much stricter:

- **Business Only:** As of May 2025, Spotify generally only accepts extension requests from **registered business entities**.
- **The 250k Rule:** They now look for apps with at least **250,000 Monthly Active Users (MAUs)** before granting a public quota.
- **Review Process:** If you do apply, they will manually review your app. Since your app's purpose is to help users _leave_ Spotify for YouTube Music, there is a high chance they would reject a public quota request anyway, as it doesn't align with their goal of "user retention."

### 3. Your "Grey Area" Workarounds

If you really want to help all 30 friends, you have a few options that don't involve a corporate registration:

- **The "Two-App" Strategy:** You can create a second app in the Spotify Developer Dashboard. This gives you another Client ID/Secret and another 25 slots. You’d just have to give 5 of your friends the second set of login credentials. (Note: This is technically a "circumvention" of their limits, but common for small private groups).
- **The "Local Script" Approach:** Instead of hosting a website where friends log in, you could provide them with a simple Python script or a "Colab" notebook. They would each create their _own_ Spotify Developer App (taking 2 minutes) and run the code locally. This bypasses your 25-user limit entirely because each friend is technically their own "developer."
- **Rotation:** You can remove friends from your allowlist once they have finished their migration to make room for new ones.

### 4. Important Technical Note

Make sure your friends know that **Development Mode** is case-sensitive. When you add their emails to the dashboard, they must match the email on their Spotify profile exactly, or they'll get that 403 error.
