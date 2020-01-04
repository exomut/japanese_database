from xml.etree.ElementTree import Element


def findall_to_csv(xml_obj: Element, find: str, divider: str = ',') -> str:
    """
    Gets text from a list of found elements and creates a divider separated string from found values.

    :param xml_obj: Element XML Element object
    :param find: str Sub element to find
    :param divider: str Defaults to ','
    :return: Returns a string of divider separated values
    :rtype: str
    """
    return divider.join([x.text for x in xml_obj.findall(find)])


def get_element_text(xml_obj: Element, default: str = '') -> str:
    """
    Get the text from an element else return default string if element is None

    :param xml_obj: Element to get text from
    :param default: str Value to return if Element is None
    :return: Text found in element
    :rtype: str
    """
    if xml_obj is not None:
        return xml_obj.text

    return default


def find_element_text(xml_obj: Element, find: str, default: str = '') -> str:
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


def is_element(element: Element) -> bool:
    """
    Checks if element is not None. Element Tree objects are Falsy if no children found.

    :param element: ElementTree.Element to check
    :return: Returns if element exists or not
    :rtype: bool
    """
    return type(element) == Element
