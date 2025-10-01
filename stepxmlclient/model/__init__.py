import xml.etree.ElementTree as ET

class BaseObject:
    _GROUP_NAME = None
    _TAG_NAME = None
    _ATTRIBUTE_NAMES = None
    _TEXT_NAMES = None
    _VALUE_NAME = None
    _CHILDREN_NAMES = None
    
    def __init__(self, data):
        self._data = data
        return
    
    def to_element(self, parent=None):
        if parent is None:
            element = ET.Element(
                tag = self._TAG_NAME,
                attrib=self._get_attributes()
            )
        else:
            element = ET.SubElement(
                parent=parent,
                tag=self._TAG_NAME,
                attrib=self._get_attributes()
            )
        value = self._get_value()
        if value:
            element.text = value
        self._add_texts(element)
        self._add_children(element)
        return element
    
    def _get_value(self):
        if self._VALUE_NAME:
            return self._data.get(self._VALUE_NAME)    
        return
    
    def _get_attributes(self):
        attributes = {}
        if self._ATTRIBUTE_NAMES:
            for name in self._ATTRIBUTE_NAMES:
                value = self._data.get(name)
                if value is not None:
                    attributes[name] = value
        return attributes
    
    def _add_texts(self, element):
        if self._TEXT_NAMES:
            for name in self._TEXT_NAMES:
                value = self._data.get(name)
                if value is not None:
                    child = ET.SubElement(element, name)
                    child.text = value
        return
    
    def _add_children(self, element):
        if self._CHILDREN_NAMES:
            for name in self._CHILDREN_NAMES:
                child = self._data.get(name)
                if child is not None:
                    child.to_element(element)
        return
        


