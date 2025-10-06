import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
    
    def test_props(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
        html_node.props_to_html()

    def test_repr(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
        expected = "HTMLNode(h1, Hello to all!, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(html_node), expected)

