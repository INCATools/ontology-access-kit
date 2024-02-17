class ChangeHandler:
    def __init__(self, oi, file):
        self.file = file
        self.oi = oi

    def write_markdown_overview_and_summary(self, curie_or_change):
        markdown_lines = ["# Overview"]  # Start with the Overview header
        markdown_lines += [f"- {key}: {len(value)}" for key, value in curie_or_change.items()]
        markdown_list = "\n".join(markdown_lines)
        self.file.write(markdown_list + "\n\n")

    def write_markdown_table(self, header, rows):
        markdown_rows = [header, "|".join(["----"] * len(header.split("|")[1:-1]))]
        markdown_rows.extend(rows)
        markdown_table = "\n".join(markdown_rows)
        self.file.write(markdown_table + "\n\n")

    def handle_new_synonym(self, value):
        rows = [
            f"| {obj.about_node} | {self.oi.label(obj.about_node)} | {obj.new_value} |"
            for obj in value
        ]
        self.file.write("### New Synonyms Added:\n\n")
        self.write_markdown_table("| ID | Label | New Synonym |", rows)

    def handle_edge_deletion(self, value):
        rows = [
            f"| {change.subject} | {self.oi.label(change.subject)} | {change.predicate} \
                | {self.oi.label(change.predicate)} | {change.object} | {self.oi.label(change.object)} |"
            for change in value
        ]
        self.file.write("### Edges Deleted:\n\n")
        self.write_markdown_table(
            "| Subject ID | Subject Label | Predicate ID | Predicate Label | Object ID | Object Label |",
            rows,
        )

    def handle_node_move(self, value):
        rows = [
            f"| {change.about_edge.subject} | {self.oi.label(change.about_edge.subject)} | \
                                {change.about_edge.predicate} | {self.oi.label(change.about_edge.predicate)} \
                                    |{change.about_edge.object} | {self.oi.label(change.about_edge.object)} |"
            for change in value
        ]
        self.file.write("### Nodes Moved:\n\n")
        self.write_markdown_table(
            "| Subject_id | Subject_label | Predicate_id | Object_id | Object_label |",
            rows,
        )

    def handle_predicate_change(self, value):
        rows = [
            f"| {change.about_edge.subject} | {self.oi.label(change.about_edge.subject)} \
                                | {change.old_value} | {change.new_value} | {change.about_edge.object} \
                                    | {self.oi.label(change.about_edge.object)} |"
            for change in value
        ]
        self.file.write("### Predicate Changed:\n\n")
        self.write_markdown_table(
            "| Subject ID | Subject Label | Old Predicate | New Predicate | Object ID | Object Label |",
            rows,
        )

    def handle_node_rename(self, value):
        rows = [
            f"| {change.about_node} | {change.old_value} | {change.new_value} |" for change in value
        ]
        self.file.write("### Node Renamed:\n\n")
        self.write_markdown_table("| ID | Old Label | New Label |", rows)

    def handle_remove_synonym(self, value):
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} |"
            for change in value
        ]
        self.file.write("### Synonyms Removed:\n\n")
        self.write_markdown_table("| ID | Label | Removed Synonym |", rows)

    def hand_synonym_predicate_change(self, value):
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} \
                                | {change.old_value} | {change.new_value} |"
            for change in value
        ]
        self.file.write("### Synonym Predicate Changed:\n\n")
        self.write_markdown_table("| ID | Label | Old Synonym | New Synonym |", rows)

    def handle_node_text_definition_change(self, value):
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} \
                                | {change.new_value} |"
            for change in value
        ]
        self.file.write("### Node Text Definition Changed:\n\n")
        self.write_markdown_table(
            "| ID | Label | Old Text Definition | New Text Definition |", rows
        )

    def handle_node_text_definition(self, value):
        rows = [
            f"| {change.about_node} | {self.oi.label(change.about_node)} | {change.old_value} \
                                | {change.new_value} |"
            for change in value
        ]
        self.file.write("### Node Text Definition Added:\n\n")
        self.write_markdown_table(
            "| ID | Label | Old Text Definition | New Text Definition |", rows
        )

    def handle_node_unobsoletion(self, value):
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]
        self.file.write("### Node Unobsoleted:\n\n")
        self.write_markdown_table("| ID | Label |", rows)

    def handle_node_creation(self, value):
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]
        self.file.write("### Node Created:\n\n")
        self.write_markdown_table("| ID | Label |", rows)

    def handle_class_creation(self, value):
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]
        self.file.write("### Class Created:\n\n")
        self.write_markdown_table("| ID | Label |", rows)

    def handle_node_deletion(self, value):
        rows = [f"| {change.about_node} | {self.oi.label(change.about_node)} |" for change in value]
        self.file.write("### Nodes Deleted:\n\n")
        self.write_markdown_table("| ID | Label |", rows)

    def handle_obsoletion(self, value):
        # Implement obsoletion handling logic here
        pass

    def handle_datatype_or_language_tag_change(self, value):
        # Implement datatype or language tag change handling logic here
        pass

    def handle_language_tag_change(self, value):
        # Implement language tag change handling logic here
        pass

    def handle_datatype_change(self, value):
        # Implement datatype change handling logic here
        pass

    def handle_allows_automatic_replacement_of_edges(self, value):
        # Implement allows automatic replacement of edges handling logic here
        pass

    def handle_unobsoletion(self, value):
        # Implement unobsoletion handling logic here
        pass

    def handle_deletion(self, value):
        # Implement deletion handling logic here
        pass

    def handle_creation(self, value):
        # Implement creation handling logic here
        pass

    def handle_subset_membership_change(self, value):
        # Implement subset membership change handling logic here
        pass

    def handle_add_to_subset(self, value):
        # Implement add to subset handling logic here
        pass

    def handle_remove_from_subset(self, value):
        # Implement remove from subset handling logic here
        pass

    def handle_edge_change(self, value):
        # Implement edge change handling logic here
        pass

    def handle_edge_creation(self, value):
        # Implement edge creation handling logic here
        pass

    def handle_place_under(self, value):
        # Implement place under handling logic here
        pass

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
            "Obsoletion": self.handle_obsoletion,
            "DatatypeOrLanguageTagChange": self.handle_datatype_or_language_tag_change,
            "LanguageTagChange": self.handle_language_tag_change,
            "DatatypeChange": self.handle_datatype_change,
            "AllowsAutomaticReplacementOfEdges": self.handle_allows_automatic_replacement_of_edges,
            "Unobsoletion": self.handle_unobsoletion,
            "Deletion": self.handle_deletion,
            "Creation": self.handle_creation,
            "SubsetMembershipChange": self.handle_subset_membership_change,
            "AddToSubset": self.handle_add_to_subset,
            "RemoveFromSubset": self.handle_remove_from_subset,
            "EdgeChange": self.handle_edge_change,
            "EdgeCreation": self.handle_edge_creation,
            "PlaceUnder": self.handle_place_under,
            # ... Add other mappings to handlers ...
        }

        for key, value in curie_or_change.items():
            handler = dispatch_table.get(key)
            if handler:
                handler(value)
            else:
                # Handle unknown case or log a warning
                print(f"No handler for key: {key}")
