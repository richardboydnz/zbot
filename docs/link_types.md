- **URLs in `href` attributes:**
  - `<a>` tags for hyperlinks
  - `<link>` tags for linked resources (stylesheets, icons, etc.)
  - `<area>` tags within image maps
  - `<base>` tags for base URL specification

- **URLs in `src` attributes:**
  - `<img>` tags for images
  - `<script>` tags for JavaScript files
  - `<iframe>` tags for embedded content
  - `<embed>` tags for embedded objects like Flash
  - `<audio>` and `<video>` tags for media files
  - `<source>` tags for specifying multiple media sources
  - `<input>` tags of type "image" for image-based submit buttons

- **URLs requiring JavaScript execution:**
  - Inline JavaScript code that dynamically sets or changes URLs
  - JavaScript that interacts with the DOM to insert or modify URLs
  - WebSocket connections initiated via JavaScript
  - Service worker registration via JavaScript
  - External JavaScript files that may contain URLs

- **Other URL sources:**
  - `action` attribute in `<form>` tags for form submission endpoints
  - `data` attribute in `<object>` tags for embedded content
  - CSS `@import` statements for including additional stylesheets
  - CSS `url()` within `<style>` tags or `style` attributes for resources like background images, fonts, etc.
  - `manifest` attribute on `<html>` tag for web application manifest files
  - `xlink:href` attribute in SVG elements for linking to other SVG resources
  - Custom data attributes (e.g., `data-background`) potentially storing URLs for JavaScript use
  - Meta tags with `content` attribute pointing to URLs (e.g., for refresh redirects or social media integration)

A meta tag with http-equiv="refresh" can contain a URL for redirection after a specified number of seconds, which is navigable once the redirection takes place.
JavaScript Navigation:

URLs embedded within JavaScript code that, when executed, can cause the browser to navigate to a new page (e.g., window.location.href = 'http://www.example.com';).
<button> or <input> Tags with Form Actions:

Buttons within forms can trigger navigation to the URL specified in the form's action attribute when clicked.
CSS Navigation:

This is less common, but CSS can be used to create clickable areas that, when combined with JavaScript, can navigate to a URL.
SVG Links:

SVG elements can use the xlink:href attribute to create links that users can navigate to.


# Mozilla attributes
https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes

Here is the markdown table for HTML attributes that can contain URLs, along with their descriptions and applicable elements:

| Attribute Name | Elements | Description |
| -------------- | -------- | ----------- |
| `action` | `<form>` | The URI of a program that processes the information submitted via the form. |
| `background` | `<body>`, `<table>`, `<td>`, `<th>` | Specifies the URL of an image file. Note: This attribute is obsolete. Use CSS `background-image` instead. |
| `cite` | `<blockquote>`, `<del>`, `<ins>`, `<q>` | Contains a URI which points to the source of the quote or change. |
| `data` | `<object>` | Specifies the URL of the resource. |
| `href` | `<a>`, `<area>`, `<base>`, `<link>` | The URL of a linked resource. |
| `manifest` | `<html>` | Specifies the URL of the document's cache manifest. Note: This attribute is obsolete, use `<link rel="manifest">` instead. |
| `poster` | `<video>` | A URL indicating a poster frame to show until the user plays or seeks. |
| `src` | `<audio>`, `<embed>`, `<iframe>`, `<img>`, `<input>`, `<script>`, `<source>`, `<track>`, `<video>` | The URL of the embeddable content. |
| `srcdoc` | `<iframe>` | - |
| `srcset` | `<img>`, `<source>` | One or more responsive image candidates. |
| `formaction` | `<input>`, `<button>` | Indicates the action of the element, overriding the action defined in the `<form>`. |
| `ping` | `<a>`, `<area>` | The `ping` attribute specifies a space-separated list of URLs to be notified if a user follows the hyperlink. |

This table includes attributes that are directly associated with URLs, such as `href` and `src`, and attributes that can override form actions like `formaction`.


# W3 Schools attributes
https://www.w3schools.com/tags/ref_attributes.asp

Certainly! Here's the information formatted as a Markdown table:

| Attribute   | Belongs to                                           | Description                                                                                               |
|-------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `action`    | `<form>`                                             | Specifies where to send the form-data when a form is submitted.                                           |
| `cite`      | `<blockquote>`, `<del>`, `<ins>`, `<q>`              | Specifies a URL which explains the quote/deleted/inserted text.                                           |
| `data`      | `<object>`                                           | Specifies the URL of the resource to be used by the object.                                               |
| `formaction`| `<input>`, `<button>`                                | Specifies where to send the form-data when a form is submitted (only for type="submit").                  |
| `href`      | `<a>`, `<area>`, `<base>`, `<link>`                  | Specifies the URL of the page the link goes to.                                                           |
| `poster`    | `<video>`                                            | Specifies an image to be shown while the video is downloading, or until the user hits the play button.   |
| `src`       | `<audio>`, `<embed>`, `<iframe>`, `<img>`, `<input>`, `<script>`, `<source>`, `<track>`, `<video>` | Specifies the URL of the media file.                                                                      |
| `srcdoc`    | `<iframe>`                                           | Specifies the HTML content of the page to show in the `<iframe>`.                                         |
| `srcset`    | `<img>`, `<source>`                                  | Specifies the URL of the image to use in different situations.                                            |
| `usemap`    | `<img>`, `<object>`                                  | Specifies an image as a client-side image map.                                                            |

This table provides a clear overview of the specific HTML attributes that may contain URLs, along with their respective tags and purposes.

# Combined with link typeBased on our discussion, here's the revised table that categorizes each attribute with the appropriate link type:

| Attribute   | Elements                                    | Link Type  |
|-------------|---------------------------------------------|------------|
| `action`    | `<form>`                                    | webpage    |
| `background`| `<body>`, `<table>`, `<td>`, `<th>`         | resource   |
| `cite`      | `<blockquote>`, `<del>`, `<ins>`, `<q>`     | other_url  |
| `data`      | `<object>`                                  | resource   |
| `formaction`| `<input>`, `<button>`                       | webpage    |
| `href`      | `<a>`, `<area>`                             | webpage    |
| `href`      | `<link>` (when linking to stylesheets, favicons, etc.) | resource   |
| `manifest`  | `<html>`                                    | resource   |
| `poster`    | `<video>`                                   | resource   |
| `src`       | `<iframe>`                                  | webpage    |
| `src`       | `<img>`, `<source>`, `<track>`, `<video>`, `<audio>`, `<embed>` | resource   |
| `src`       | `<script>`                                  | script     |
| `src`       | `<input>` (type="image")                    | resource   |
| `srcdoc`    | `<iframe>`                                  | other_url  |
| `srcset`    | `<img>`, `<source>`                         | resource   |
| `ping`      | `<a>`, `<area>`                             | other_url  |
| `usemap`    | `<img>`, `<object>`                         | other_url  |

This table reflects the following understandings:

- The `src` attribute for `<iframe>` is categorized as a link to a webpage.
- The `src` attribute for `<img>` and similar elements is categorized as linking to a resource.
- The `cite` attribute is categorized under "other_url" as it can refer to various types of citations.
- The `data` attribute is considered a link to a resource.
- The `href` attribute in `<a>` and `<area>` tags is typically a link to a webpage, while in `<link>` tags, it's used for resources like stylesheets or favicons.

This categorization is more aligned with the standard uses of these attributes in HTML.

## no variability

Here's a table of HTML attributes with URLs where the link type does not have significant variability:

| Attribute   | Elements                                    | Link Type  |
|-------------|---------------------------------------------|------------|
| `background`| `<body>`, `<table>`, `<td>`, `<th>`         | resource   |
| `href`      | `<a>`, `<area>`                             | webpage    |
| `manifest`  | `<html>`                                    | resource   |
| `poster`    | `<video>`                                   | resource   |
| `src`       | `<iframe>`                                  | webpage    |
| `src`       | `<img>`, `<source>`, `<track>`, `<video>`, `<audio>`, `<embed>` | resource   |
| `src`       | `<script>`                                  | script     |
| `srcdoc`    | `<iframe>`                                  | other_url  |
| `srcset`    | `<img>`, `<source>`                         | resource   |
| `ping`      | `<a>`, `<area>`                             | other_url  |
| `usemap`    | `<img>`, `<object>`                         | other_url  |

In this table:

- Attributes like `background`, `poster`, `src` (for images, videos, etc.), and `srcset` are consistently linked to resources, typically images or media files.
- The `href` attribute in `<a>` and `<area>` tags is typically used for linking to webpages.
- The `src` attribute for `<iframe>` is usually a webpage link, and for `<script>`, it's a script link.
- `srcdoc` in `<iframe>`, `ping`, and `usemap` are categorized as "other_url" due to their specific or varied usage. 

This table focuses on attributes where the link type is largely consistent and does not vary significantly based on context or usage.

## variability

Certainly! Let's create a table that specifically highlights attributes with variable link types, discusses their variability, and suggests methods for determining the appropriate link type based on further information.

| Attribute   | Elements                                    | Potential Link Types       | Variability Discussion                                                                                  | Deciding on Link Type                                 |
|-------------|---------------------------------------------|----------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| `action`    | `<form>`                                    | webpage, webapp            | Depends on whether the form submission is to a crawlable webpage or a web application endpoint.       | Check the form's `method` (GET indicates a webpage; POST often indicates a webapp). Examine the form's context and purpose. |
| `formaction`| `<input>`, `<button>`                       | webpage, webapp            | Similar to `action`, it depends on the nature of the form submission endpoint.                         | Same as above. Look at the button/input's form method and its context.             |
| `cite`      | `<blockquote>`, `<del>`, `<ins>`, `<q>`     | webpage, other_url         | Can reference a webpage or any other URL providing context or source.                                  | Examine the context of the citation to determine the nature of the URL.           |
| `data`      | `<object>`                                  | resource, webpage, script  | Used for various types of resources including media, embedded content, or scripts.                     | Look at the type of object being embedded to determine the link type.             |
| `href`      | `<link>`                                    | resource, style, other_url | Commonly used for stylesheets and resources, but can have other uses in specific contexts.             | Examine the `rel` attribute of the link and the context in which it's used.       |
| `src`       | `<input>` (type="image")                    | resource, webpage          | Typically used for image resources, but can be used in contexts where the link type might vary.        | Consider how the image input is used within the form.                            |

This table highlights the attributes where the link type can vary and provides guidance on how to determine the appropriate type. The decision often hinges on examining the specific context and purpose of the attribute in the HTML document. For instance, the method of a form (`GET` or `POST`) can suggest whether `action` or `formaction` points to a crawlable webpage or a web application endpoint. Similarly, the `rel` attribute in a `<link>` tag can provide clues about the nature of the `href` link.

Relative to absolute:
https://docs.scrapy.org/en/latest/topics/request-response.html
> urljoin(url)[source]¶
Constructs an absolute url by combining the Response’s base url with a possible relative url. The base url shall be extracted from the <base> tag, or just the Response’s url if there is no such tag.

