from xml.etree.ElementTree import Element


def is_element(element: Element) -> bool:
    """
    Checks if element is not None. Element Tree objects are Falsy if no children found.

    :param element: ElementTree.Element to check
    :return: Returns if element exists or not
    :rtype: bool
    """
    return type(element) == Element


def get_element_text(xml_obj: Element, find: str, default: str = '') -> str:
    """
    Finds sub elements in the given element and returns the text if found or default string.

    :param xml_obj: Element XML Element object
    :param find: str Sub element to find
    :param default: str Text to return if no elements found
    :return: Found text of Default string
    :rtype: str
    """
    element = xml_obj.find(find)

    if is_element(element):
        return element.text

    return default
