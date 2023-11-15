example_html = """<!DOCTYPE html>
<html manifest="site.manifest">
<head>
    <title>©My Complex Web Page</title>
    <script src="script.js"></script>
    <style>
        body { background: url('background.jpg'); }
        header, footer { background: lightgray; padding: 10px; text-align: center; }
        nav a { margin: 0 10px; }
        aside { background: #f0f0f0; padding: 10px; }
        main { padding: 20px; }
        video, img, audio, object { display: block; margin-top: 20px; }
    </style>
</head>
<body>
    <header>
        <h1>Welcome to My Web Page</h1>
        <nav>
            <a href="page1.html">Home</a>
            <a href="page2.html">About Us</a>
            <a href="page3.html">Services</a>
            <a href="page4.html">Contact</a>
        </nav>
    </header>
    
    <aside>
        <h3>Special Offer!</h3>
        <p>Don't miss our exclusive offer at <a href="https://www.example.com" ping="tracker.php">Example.com</a></p>
    </aside>

    <main>
        <section>
            <h2>Our Mission</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <iframe src="frame.html" width="300" height="200"></iframe>
            <iframe srcdoc="&lt;p&gt;Inline HTML content here.&lt;/p&gt;" width="300" height="200"></iframe>
        </section>
        <article>
            <h2>Featured Content</h2>
            <video poster="poster.jpg" controls width="400">
                <source src="video.mp4" type="video/mp4">
                <track src="subtitles_en.vtt" kind="subtitles" srclang="en" label="English">
                Your browser does not support the video tag.
            </video>
            <img src="photo.jpg" srcset="photo.jpg 1x, photo@2x.jpg 2x" usemap="#imagemap" alt="Image with Map" width="400">
            <map name="imagemap">
                <area shape="rect" coords="34,44,270,350" href="linked.html" alt="Linked Area">
            </map>
            <audio src="audio.mp3" controls>Your browser does not support the audio element.</audio>
            <object data="embedded.swf" type="application/x-shockwave-flash" width="400" height="300">Flash content cannot be displayed.</object>
        </article>
    </main>

    <footer>
        <p>© 2023 My Complex Web Page. All rights reserved.</p>
    </footer>
</body>
</html>
"""