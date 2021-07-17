"""
Provides customised XML rendering support.
"""
from io import StringIO

from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework_xml.renderers import XMLRenderer


class CustomXMLRenderer(XMLRenderer):
    """Custom XML render for the app."""
    root_contents_key = None

    @staticmethod
    def select_valid_property_names(data, clear_from_data=False):
        """Filters properties from the provided data that are strings."""
        selected_properties = {}
        for key, value in data.items():
            if isinstance(value, str):
                selected_properties[key] = value

        if clear_from_data:
            for key in selected_properties: del data[key]
        return selected_properties

    def render_body(self, xml, data):
        raise NotImplemented

    def create_element_with_properties(self, xml, data, contents):
        """Creates an XML object with provided data."""
        if not isinstance(data, dict):
            return xml

        selected_properties = self.select_valid_property_names(data, clear_from_data=True)
        xml.addQuickElement('outcode', contents, selected_properties)
        return xml

    def parse_root(self, xml, data):
        """Adds root xml element to the xml response"""
        data_contents = None
        if self.root_contents_key:
            data_contents = data.pop(self.root_contents_key, None)

        selected_properties = self.select_valid_property_names(data, clear_from_data=True)
        xml.startElement(self.root_tag_name, selected_properties)
        xml.characters(data_contents)
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

        xml = self.parse_root(xml, data)
        xml = self.render_body(xml, data)

        xml.endDocument()
        return stream.getvalue()


class OutcodeXMLRenderer(CustomXMLRenderer):
    """Parse outcode data to an XML response."""
    root_tag_name = 'outcode'
    root_contents_key = 'id'

    def render_body(self, xml, data):
        """Parse outcode view to an XML response."""
        xml.endElement(self.root_tag_name)
        return xml


class OutcodesXMLRenderer(CustomXMLRenderer):
    """Parse outcodes data to an XML response."""
    root_tag_name = 'outcodes'
    root_contents_key = 'id'

    def render_body(self, xml, data):
        """Parse outcodes data to an XML response."""
        outcodes = data.get('outcodes', [])
        for outcode in outcodes:
            contents = outcode.pop('id', None)
            self.create_element_with_properties(xml, outcode, contents)
        xml.endElement(self.root_tag_name)
        return xml
