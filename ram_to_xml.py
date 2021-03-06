from metadata import Schema, Constraint, Domain, Field, Index, Table
import xml.dom.minidom as md

def ram_to_xml(schema):

    if schema is None:
        raise ValueError("Schema is None")

    xml = md.Document()

    xmlModel = xml.createElement("dbd_schema")

    if schema.fulltext_engine is not None:
        xmlModel.setAttribute("fulltext_engine", schema.fulltext_engine)
    if schema.version is not None:
        xmlModel.setAttribute("version", schema.version)
    if schema.name is not None:
        xmlModel.setAttribute("name", schema.name)
    if schema.description is not None:
        xmlModel.setAttribute("description", schema.description)
    xmlModel.appendChild(xml.createElement("custom"))

    domains = xml.createElement("domains")
    for domain in getRAMDomains(xml, schema.domains):
        domains.appendChild(domain)
    xmlModel.appendChild(domains)

    tables = xml.createElement("tables")
    for table in getRAMTables(xml, schema.tables):
        tables.appendChild(table)
    xmlModel.appendChild(tables)

    xml.appendChild(xmlModel)

    return xml

def getRAMDomains(xml, domains):

    for domain in domains:
        node = xml.createElement("domain")
        if domain.name is not None:
            node.setAttribute("name", domain.name)
        if domain.description is not None:
            node.setAttribute("description", domain.description)
        if domain.type is not None:
            node.setAttribute("type", domain.type)
        if domain.align is not None:
            node.setAttribute("align", domain.align)
        if domain.width is not None:
            node.setAttribute("width", domain.width)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.precision is not None:
            node.setAttribute("precision", domain.precision)
        propsList = []
        if domain.show_null:
            propsList.append("show_null")
        if domain.summable:
            propsList.append("summable")
        if domain.case_sensitive:
            propsList.append("case_sensitive")
        if domain.show_lead_nulls:
            propsList.append("show_lead_nulls")
        if domain.thousands_separator:
            propsList.append("thousands_separator")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        if domain.char_length is not None:
            node.setAttribute("char_length", domain.char_length)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.scale is not None:
            node.setAttribute("scale", domain.scale)
        yield node

def getRAMTables(xml, tables):

    for table in tables:
        node = xml.createElement("table")
        if table.name is not None:
            node.setAttribute("name", table.name)
        if  table.description is not None:
            node.setAttribute("description", table.description)
        propsList = []
        if table.add:
            propsList.append("add")
        if table.edit:
            propsList.append("edit")
        if table.delete:
            propsList.append("delete")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        if table.fields != []:
            for field in getRAMFields(xml, table.fields):
                node.appendChild(field)

        if table.constraints != []:
            for constrint in getRAMConstraint(xml, table.constraints):
                node.appendChild(constrint)

        if table.indexes != []:
            for index in getRAMIndex(xml, table.indexes):
                node.appendChild(index)

        yield node

def getRAMFields(xml, fields):

    for field in fields:
        node = xml.createElement("field")
        if field.name is not None:
            node.setAttribute("name", field.name)
        if field.rname is not None:
            node.setAttribute("rname", field.rname)
        if field.domain is not None:
            node.setAttribute("domain", field.domain)
        if field.description is not None:
            node.setAttribute("description", field.description)
        propsList = []
        if field.input:
            propsList.append("input")
        if field.edit:
            propsList.append("edit")
        if field.show_in_grid:
            propsList.append("show_in_grid")
        if field.show_in_details:
            propsList.append("show_in_details")
        if field.is_mean:
            propsList.append("is_mean")
        if field.autocalculated:
            propsList.append("autocalculated")
        if field.required:
            propsList.append("required")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        yield node

def getRAMConstraint(xml, constraints):

    for constraint in constraints:
        node = xml.createElement("constraint")
        if constraint.name is not None:
            node.setAttribute("name", constraint.name)
        if constraint.kind is not None:
            node.setAttribute("kind", constraint.kind)
        if constraint.items is not None:
            node.setAttribute("items", constraint.items)
        if constraint.reference_type is not None:
            node.setAttribute("reference_type", constraint.reference_type)
        if constraint.reference is not None:
            node.setAttribute("reference", constraint.reference)
        propsList = []
        if constraint.has_value_edit:
            propsList.append("has_value_edit")
        if constraint.cascading_delete:
            propsList.append("cascading_delete")
        if constraint.full_cascading_delete:
            propsList.append("full_cascading_delete")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))
        yield node


def getRAMIndex(xml, indexes):

    for index in indexes:
        if index.fields != []:
            node = xml.createElement("index")
            # if len(index.fields) == 1:
            #    node.setAttribute("field", index.fields[0])
            # else:
            #     pass
            if index.name is not None:
                node.setAttribute("name", index.name)
            propsList = []
            if index.fulltext:
                propsList.append("fulltext")
            if index.uniqueness:
                propsList.append("uniqueness")
            if propsList != []:
                node.setAttribute("props", ", ".join(propsList))

            yield node
        else:
            raise ValueError("Error! Index does not contain fields")