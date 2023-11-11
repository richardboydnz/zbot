test_html_content: str = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="/home">Home</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </nav>
        <h1>Welcome to the Test Page</h1>
    </header>
    <aside>
        <p>This is a sidebar content.</p>
    </aside>
    <main>
        <article>
            <h2>Article Title</h2>
            <p>Article content...</p>
        </article>
    </main>
    <footer>
        <nav>
            <ul>
                <li><a href="/privacy">Privacy Policy</a></li>
                <li><a href="/terms">Terms of Service</a></li>
            </ul>
        </nav>
        <p>© 2023 Test Page</p>
    </footer>
</body>
</html>
'''
