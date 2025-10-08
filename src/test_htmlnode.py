import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class Test_HTML_Node(unittest.TestCase):
    def test_eq(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
    
    def test_props(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
        html_node.props_to_html()

    def test_repr(self):
        html_node = HTMLNode("h1", "Hello to all!", None, {"href": "https://www.google.com", "target": "_blank",})
        expected = "HTMLNode(h1, Hello to all!, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        self.assertEqual(repr(html_node), expected)

class Test_HTML_Leaf_Node(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_NOT_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node.to_html(), "<a>Hello, world!</a>")
    
    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class Test_HTML_Parent_Node(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_single_child(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p>Hello</p></div>")
    
    def test_multiple_children(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("span", "World")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>Hello</p><span>World</span></div>")
    
    def test_nested_parents(self):
        inner_child = LeafNode("span", "Nested")
        inner_parent = ParentNode("p", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><p><span>Nested</span></p></div>")

    def test_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
    
    def test_no_children_message(self):
        with self.assertRaisesRegex(ValueError, "children"):
            ParentNode("div", None).to_html()
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()