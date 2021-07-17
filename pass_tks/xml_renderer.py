"""
Provides customised XML rendering support.
"""
from io import StringIO

from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework_xml.renderers import XMLRenderer


class ListingsXMLRenderer(XMLRenderer):
    """Custom XML render for the app."""

    def __init__(self, root_tag='root', item_tag='list-item'):
        self.root_tag_name = root_tag
        self.item_tag_name = item_tag
        # before using this for other views, make sure there exists a relevant
        # parse method, otherwise create one.
        self.mappings = {
            'outcode': self.parse_outcode,
            'outcodes': self.parse_outcodes
        }

    @staticmethod
    def select_valid_property_names(data):
        """Filters properties from the provided data that are strings."""
        selected_properties = {}
        for key, value in data.items():
            if isinstance(value, str):
                selected_properties[key] = value
        return selected_properties

    def create_outcode_element_with_properties(self, xml, outcode_info):
        """Creates an XML object for provided outcode information. """
        outcode_contents = outcode_info.pop('id', None)
        selected_properties = self.select_valid_property_names(outcode_info)
        for key in selected_properties: del outcode_info[key]
        xml.addQuickElement('outcode', outcode_contents, selected_properties)
        return xml

    def parse_root(self, xml, data):
        """Adds root xml element to the xml response"""
        outcode_contents = data.pop('id', None)
        selected_properties = self.select_valid_property_names(data)
        xml.startElement(self.root_tag_name, selected_properties)
        xml.characters(outcode_contents)
        return xml

    def parse_outcodes(self, xml, data):
        """Parse outcodes view to an XML response."""
        xml = self.parse_root(xml, data)
        outcodes = data.get('outcodes', [])
        for outcode in outcodes:
            self.create_outcode_element_with_properties(xml, outcode)
        xml.endElement(self.root_tag_name)
        return xml

    def parse_outcode(self, xml, data):
        """Parse outcode view to an XML response."""
        xml = self.parse_root(xml, data)
        xml.endElement(self.root_tag_name)
        return xml

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ""

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()

        xml = self.mappings[self.root_tag_name](xml, data)

        xml.endDocument()
        return stream.getvalue()
