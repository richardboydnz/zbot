from myscraper.types.api_page import Pages
api_url: str = "https://example.com/wp-json/wp/v2/pages"
api_result: Pages = [
  {
    "id": 1001,
    "date": "2023-12-22T12:00:00",
    "date_gmt": "2023-12-22T20:00:00",
    "guid": {
      "rendered": "https://example.com/?page_id=1001"
    },
    "modified": "2023-12-22T12:00:00",
    "modified_gmt": "2023-12-22T20:00:00",
    "slug": "page-one",
    "status": "publish",
    "type": "page",
    "link": "https://example.com/page-one/",
    "title": {
      "rendered": "Page One"
    },
    "content": {
      "rendered": "<p>This is the content of Page One. Visit our other pages: <a href='https://example.com/page-two/'>Page Two</a> and <a href='https://example.com/page-three/'>Page Three</a>.</p>",
      "protected": False
    },
    "excerpt": {
      "rendered": "",
      "protected": False
    },
    "author": 1,
    "featured_media": 0,
    "parent": 0,
    "menu_order": 1,
    "comment_status": "closed",
    "ping_status": "closed",
    "template": "",
    "meta": {
      "_et_pb_use_builder": "off",
      "_et_pb_old_content": "",
      "_et_gb_content_width": ""
    },
    "_links": {
      "self": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages/1001"
        }
      ],
      "collection": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages"
        }
      ],
      "about": [
        {
          "href": "https://example.com/wp-json/wp/v2/types/page"
        }
      ],
      "author": [
        {
          "embeddable": True,
          "href": "https://example.com/wp-json/wp/v2/users/1"
        }
      ],
      "replies": [],
      "version-history": [
        {
          "count": 0,
          "href": "https://example.com/wp-json/wp/v2/pages/1001/revisions"
        }
      ],
      "wp:attachment": [],
      "curies": [
        {
          "name": "wp",
          "href": "https://api.w.org/{rel}",
          "templated": True
        }
      ]
    }
  },
  {
    "id": 1002,
    "date": "2023-12-22T13:00:00",
    "date_gmt": "2023-12-22T21:00:00",
    "guid": {
      "rendered": "https://example.com/?page_id=1002"
    },
    "modified": "2023-12-22T13:00:00",
    "modified_gmt": "2023-12-22T21:00:00",
    "slug": "page-two",
    "status": "publish",
    "type": "page",
    "link": "https://example.com/page-two/",
    "title": {
      "rendered": "Page Two"
    },
    "content": {
      "rendered": "<p>This is the content of Page Two. Go back to <a href='https://example.com/page-one/'>Page One</a>.</p>",
      "protected": False
    },
    "excerpt": {
      "rendered": "",
      "protected": False
    },
    "author": 1,
    "featured_media": 0,
    "parent": 0,
    "menu_order": 2,
    "comment_status": "closed",
    "ping_status": "closed",
    "template": "",
    "meta": {
      "_et_pb_use_builder": "off",
      "_et_pb_old_content": "",
      "_et_gb_content_width": ""
    },
    "_links": {
      "self": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages/1002"
        }
      ],
      "collection": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages"
        }
      ],
      "about": [
        {
          "href": "https://example.com/wp-json/wp/v2/types/page"
        }
      ],
      "author": [
        {
          "embeddable": True,
          "href": "https://example.com/wp-json/wp/v2/users/1"
        }
      ],
      "replies": [],
      "version-history": [
        {
          "count": 0,
          "href": "https://example.com/wp-json/wp/v2/pages/1002/revisions"
        }
      ],
      "wp:attachment": [],
      "curies": [
        {
          "name": "wp",
          "href": "https://api.w.org/{rel}",
          "templated": True
        }
      ]
    }
  },
  {
    "id": 1003,
    "date": "2023-12-22T14:00:00",
    "date_gmt": "2023-12-22T22:00:00",
    "guid": {
      "rendered": "https://example.com/?page_id=1003"
    },
    "modified": "2023-12-22T14:00:00",
    "modified_gmt": "2023-12-22T22:00:00",
    "slug": "page-three",
    "status": "publish",
    "type": "page",
    "link": "https://example.com/page-three/",
    "title": {
      "rendered": "Page Three"
    },
    "content": {
      "rendered": "<p>This is the content of Page Three. Go back to <a href='https://example.com/page-one/'>Page One</a>.</p>",
      "protected": False
    },
    "excerpt": {
      "rendered": "",
      "protected": False
    },
    "author": 1,
    "featured_media": 0,
    "parent": 0,
    "menu_order": 3,
    "comment_status": "closed",
    "ping_status": "closed",
    "template": "",
    "meta": {
      "_et_pb_use_builder": "off",
      "_et_pb_old_content": "",
      "_et_gb_content_width": ""
    },
    "_links": {
      "self": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages/1003"
        }
      ],
      "collection": [
        {
          "href": "https://example.com/wp-json/wp/v2/pages"
        }
      ],
      "about": [
        {
          "href": "https://example.com/wp-json/wp/v2/types/page"
        }
      ],
      "author": [
        {
          "embeddable": True,
          "href": "https://example.com/wp-json/wp/v2/users/1"
        }
      ],
      "replies": [],
      "version-history": [
        {
          "count": 0,
          "href": "https://example.com/wp-json/wp/v2/pages/1003/revisions"
        }
      ],
      "wp:attachment": [],
      "curies": [
        {
          "name": "wp",
          "href": "https://api.w.org/{rel}",
          "templated": True
        }
      ]
    }
  }
]