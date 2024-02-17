class ChangeHandler:
    def __init__(self, oi, file):
        self.file = file
        self.oi = oi

    def write_markdown_collapsible(self, title, content_lines):
        # Start with the details tag for a collapsible section
        self.file.write(f"<details>\n<summary>{title}</summary>\n\n")

        # Write the content lines within the collapsible section
        content = "\n".join(content_lines)
        self.file.write(content + "\n\n")

        # Close the details tag
        self.file.write("</details>\n\n")

    def write_markdown_overview_and_summary(self, curie_or_change):
        # Create the Overview content lines
        overview_lines = [f"- {key}: {len(value)}" for key, value in curie_or_change.items()]

        # Write the Overview as a collapsible section
        self.write_markdown_collapsible("Overview", overview_lines)

    def write_markdown_table(self, title, header, rows):
        # Create the table header and separator lines
        markdown_rows = [header, "|".join(["----"] * len(header.split("|")[1:-1]))]

        # Add the table rows
        markdown_rows.extend(rows)

        # Write the table as a collapsible section
        self.write_markdown_collapsible(title, markdown_rows)

    def handle_new_synonym(self, value):
        # Create rows for the table
        rows = [
            f"| {obj.about_node} | {self.oi.label(obj.about_node)} | {obj.new_value} |"
            for obj in value
        ]

        # Define the header for the table
        header = "| ID | Label | New Synonym |"

        # Write the "New Synonyms Added" section as a collapsible markdown table
        self.write_markdown_table("New Synonyms Added", header, rows)

    def handle_edge_deletion(self, value):
        # Create rows for the table
        rows = [
            f"| {change.subject} | {self.oi.label(change.subject)} | {change.predicate} \
                | {self.oi.label(change.predicate)} | {change.object} | {self.oi.label(change.object)} |"
            for change in value
        ]

        # Define the header for the table
        header = "| Subject ID | Subject Label | Predicate ID | Predicate Label | Object ID | Object Label |"

        # Write the "Edges Deleted" section as a collapsible markdown table
        self.write_markdown_table("Edges Deleted", header, rows)

    def handle_node_move(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_edge.subject} | {self.oi.label(change.about_edge.subject)} | \
                {change.about_edge.predicate} | {self.oi.label(change.about_edge.predicate)} \
                    |{change.about_edge.object} | {self.oi.label(change.about_edge.object)} |"
            for change in value
        ]

        # Define the header for the table
        header = "| Subject_id | Subject_label | Predicate_id | Object_id | Object_label |"

        # Write the "Nodes Moved" section as a collapsible markdown table
        self.write_markdown_table("Nodes Moved", header, rows)

    def handle_predicate_change(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_edge.subject} | {self.oi.label(change.about_edge.subject)} \
                | {change.old_value} | {change.new_value} | {change.about_edge.object} \
                    | {self.oi.label(change.about_edge.object)} |"
            for change in value
        ]

        # Define the header for the table
        header = "| Subject ID | Subject Label | Old Predicate | New Predicate | Object ID | Object Label |"

        # Write the "Predicate Changed" section as a collapsible markdown table
        self.write_markdown_table("Predicate Changed", header, rows)

    def handle_node_rename(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {change.old_value} | {change.new_value} |" for change in value
        ]

        # Define the header for the table
        header = "| ID | Old Label | New Label |"

        # Write the "Node Renamed" section as a collapsible markdown table
        self.write_markdown_table("Node Renamed", header, rows)

    def handle_remove_synonym(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} |"
            for change in value
        ]

        # Define the header for the table
        header = "| ID | Label | Removed Synonym |"

        # Write the "Synonyms Removed" section as a collapsible markdown table
        self.write_markdown_table("Synonyms Removed", header, rows)

    def hand_synonym_predicate_change(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} \
                | {change.old_value} | {change.new_value} |"
            for change in value
        ]

        # Define the header for the table
        header = "| ID | Label | Old Synonym | New Synonym |"

        # Write the "Synonym Predicate Changed" section as a markdown table
        self.write_markdown_table("Synonym Predicate Changed", header, rows)

    def handle_node_text_definition_change(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} \
                | {change.new_value} |"
            for change in value
        ]

        # Define the header for the table
        header = "| ID | Label | Old Text Definition | New Text Definition |"

        # Write the "Node Text Definition Changed" section as a markdown table
        self.write_markdown_table("Node Text Definition Changed", header, rows)

    def handle_node_text_definition(self, value):
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} \
                | {change.new_value} |"
            for change in value
        ]

        # Define the header for the table
        header = "| ID | Label | Old Text Definition | New Text Definition |"

        # Write the "Node Text Definition Added" section as a markdown table
        self.write_markdown_table("Node Text Definition Added", header, rows)

    def handle_node_unobsoletion(self, value):
        # Create rows for the table
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]

        # Define the header for the table
        header = "| ID | Label |"

        # Write the "Node Unobsoleted" section as a markdown table
        self.write_markdown_table("Node Unobsoleted", header, rows)

    def handle_node_creation(self, value):
        # Create rows for the table
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]

        # Define the header for the table
        header = "| ID | Label |"

        # Write the "Node Created" section as a markdown table
        self.write_markdown_table("Node Created", header, rows)

    def handle_class_creation(self, value):
        # Create rows for the table
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]

        # Define the header for the table
        header = "| ID | Label |"

        # Write the "Class Created" section as a markdown table
        self.write_markdown_table("Class Created", header, rows)

    def handle_node_deletion(self, value):
        # Create rows for the table
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]

        # Define the header for the table
        header = "| ID | Label |"

        # Write the "Nodes Deleted" section as a markdown table
        self.write_markdown_table("Nodes Deleted", header, rows)

    def handle_new_text_definition(self, value):
        import pdb

        pdb.set_trace()
        # Create rows for the table
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.new_value} |"
            for change in value
        ]
        header = "| ID | Label | New Text Definition |"
        self.write_markdown_table("New Text Definition", header, rows)

    # def handle_obsoletion(self, value):
    #     # Implement obsoletion handling logic here
    #     pass

    # def handle_datatype_or_language_tag_change(self, value):
    #     # Implement datatype or language tag change handling logic here
    #     pass

    # def handle_language_tag_change(self, value):
    #     # Implement language tag change handling logic here
    #     pass

    # def handle_datatype_change(self, value):
    #     # Implement datatype change handling logic here
    #     pass

    # def handle_allows_automatic_replacement_of_edges(self, value):
    #     # Implement allows automatic replacement of edges handling logic here
    #     pass

    # def handle_unobsoletion(self, value):
    #     # Implement unobsoletion handling logic here
    #     pass

    # def handle_deletion(self, value):
    #     # Implement deletion handling logic here
    #     pass

    # def handle_creation(self, value):
    #     # Implement creation handling logic here
    #     pass

    # def handle_subset_membership_change(self, value):
    #     # Implement subset membership change handling logic here
    #     pass

    # def handle_add_to_subset(self, value):
    #     # Implement add to subset handling logic here
    #     pass

    # def handle_remove_from_subset(self, value):
    #     # Implement remove from subset handling logic here
    #     pass

    # def handle_edge_change(self, value):
    #     # Implement edge change handling logic here
    #     pass

    # def handle_edge_creation(self, value):
    #     # Implement edge creation handling logic here
    #     pass

    # def handle_place_under(self, value):
    #     # Implement place under handling logic here
    #     pass

    def process_changes(self, curie_or_change):
        # Write overview and summary at the beginning of the document
        self.write_markdown_overview_and_summary(curie_or_change)
        dispatch_table = {
            "NewSynonym": self.handle_new_synonym,
            "EdgeDeletion": self.handle_edge_deletion,
            "NodeMove": self.handle_node_move,
            "PredicateChange": self.handle_predicate_change,
            "NodeRename": self.handle_node_rename,
            "RemoveSynonym": self.handle_remove_synonym,
            "SynonymPredicateChange": self.hand_synonym_predicate_change,
            "NodeTextDefinitionChange": self.handle_node_text_definition_change,
            "NodeTextDefinition": self.handle_node_text_definition,
            "NodeUnobsoletion": self.handle_node_unobsoletion,
            "NodeCreation": self.handle_node_creation,
            "ClassCreation": self.handle_class_creation,
            "NodeDeletion": self.handle_node_deletion,
            "NewTextDefinition": self.handle_new_text_definition,
            # "Obsoletion": self.handle_obsoletion,
            # "DatatypeOrLanguageTagChange": self.handle_datatype_or_language_tag_change,
            # "LanguageTagChange": self.handle_language_tag_change,
            # "DatatypeChange": self.handle_datatype_change,
            # "AllowsAutomaticReplacementOfEdges": self.handle_allows_automatic_replacement_of_edges,
            # "Unobsoletion": self.handle_unobsoletion,
            # "Deletion": self.handle_deletion,
            # "Creation": self.handle_creation,
            # "SubsetMembershipChange": self.handle_subset_membership_change,
            # "AddToSubset": self.handle_add_to_subset,
            # "RemoveFromSubset": self.handle_remove_from_subset,
            # "EdgeChange": self.handle_edge_change,
            # "EdgeCreation": self.handle_edge_creation,
            # "PlaceUnder": self.handle_place_under,
            # ... Add other mappings to handlers ...
        }

        for key, value in curie_or_change.items():
            handler = dispatch_table.get(key)
            if handler:
                handler(value)
            else:
                # Handle unknown case or log a warning
                print(f"No handler for key: {key}")
