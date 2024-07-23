"""Change Handler Class."""

from dataclasses import dataclass
from typing import Dict, List

from kgcl_schema.datamodel.kgcl import Change


@dataclass
class ChangeHandler:
    def __init__(self, oi, file):
        self.file = file
        self.oi = oi

    def write_markdown_collapsible(self, title: str, content_lines: List[str]) -> None:
        self.file.write(f"<details>\n<summary>{title}</summary>\n\n")
        self.file.write("\n".join(content_lines) + "\n\n")
        self.file.write("</details>\n\n")

    def write_markdown_table(self, title: str, header: str, rows: List[str]) -> None:
        separator = "|".join(["----"] * len(header.split("|")[1:-1])) + "|"
        markdown_rows = [header, separator] + rows
        self.write_markdown_collapsible(title, markdown_rows)

    def handle_generic_change(
        self, value: List[object], title: str, header: str, row_format: str
    ) -> None:
        rows = list({row_format.format(change=change) for change in value})
        self.write_markdown_table(f"{title}: {len(rows)}", header, rows)

    def handle_new_synonym(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(obj.about_node)} | {obj.new_value} | {obj.predicate} |"
                for obj in value
            }
        )

        # Define the header for the table
        header = "| Term | New Synonym | Predicate |"

        # Write the "New Synonyms Added" section as a collapsible markdown table
        self.write_markdown_table(f"Synonyms added: {len(rows)}", header, rows)

    def handle_edge_deletion(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.subject)} | {self._format_entity_labels(change.predicate)} |\
                {self._format_entity_labels(change.object)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject| Predicate| Object|"

        # Write the "Edges Deleted" section as a collapsible markdown table
        self.write_markdown_table(f"Relationships removed: {len(rows)}", header, rows)

    def handle_edge_creation(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.subject)} | {self._format_entity_labels(change.predicate)} |\
                {self._format_entity_labels(change.object)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject | Predicate | Object|"

        # Write the "Edges Created" section as a collapsible markdown table
        self.write_markdown_table(f"Relationships added: {len(rows)}", header, rows)

    def handle_edge_change(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_edge.subject)} | \
                {self._format_entity_labels(change.about_edge.predicate)} | \
                {self._format_entity_labels(change.old_value)} | {self._format_entity_labels(change.new_value)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject | Predicate | Old Object | New Object |"

        # Write the "Edges Changed" section as a collapsible markdown table
        self.write_markdown_table(f"Relationships changed: {len(rows)}", header, rows)

    def handle_node_move(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_edge.subject)} | \
                {self._format_entity_labels(change.about_edge.predicate)} |\
                {self._format_entity_labels(change.about_edge.object)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject | Predicate | Object |"

        # Write the "Nodes Moved" section as a collapsible markdown table
        self.write_markdown_table(f"Relationships added: {len(rows)}", header, rows)

    def handle_predicate_change(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_edge.subject)} | \
                {self._format_entity_labels(change.old_value)} |\
                {self._format_entity_labels(change.new_value)} | \
                {self._format_entity_labels(change.about_edge.object)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject | Old Predicate | New Predicate | Object |"

        # Write the "Predicate Changed" section as a collapsible markdown table
        self.write_markdown_table(f"Predicates changed: {len(rows)}", header, rows)

    def handle_node_rename(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {change.about_node} | {change.old_value} | {change.new_value} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| ID | Old Label | New Label |"

        # Write the "Node Renamed" section as a collapsible markdown table
        self.write_markdown_table(f"Nodes renamed: {len(rows)}", header, rows)

    def handle_remove_synonym(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.old_value} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Term | Removed Synonym |"

        # Write the "Synonyms Removed" section as a collapsible markdown table
        self.write_markdown_table(f"Synonyms removed: {len(rows)}", header, rows)

    def hand_synonym_predicate_change(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.old_value} |\
                  {change.new_value} | {change.target} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Term | Old Predicate | New Predicate | Synonym |"

        # Write the "Synonym Predicate Changed" section as a markdown table
        self.write_markdown_table(f"Synonym predicates changed: {len(rows)}", header, rows)

    def handle_node_text_definition_change(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.old_value} |\
                  {change.new_value} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Term | Old Text Definition | New Text Definition |"

        # Write the "Node Text Definition Changed" section as a markdown table
        self.write_markdown_table(f"Text definitions changed: {len(rows)}", header, rows)

    def handle_node_text_definition(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.old_value} |\
                  {change.new_value} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Term | Old Text Definition | New Text Definition |"

        # Write the "Node Text Definition Added" section as a markdown table
        self.write_markdown_table(f"Text definitions added: {len(rows)}", header, rows)

    def handle_node_unobsoletion(self, value: List[Change]):
        # Create rows for the table
        rows = list({f"| {self._format_entity_labels(change.about_node)} |" for change in value})

        # Define the header for the table
        header = "| Term |"

        # Write the "Node Unobsoleted" section as a markdown table
        self.write_markdown_table(f"Nodes unobsoleted: {len(rows)}", header, rows)

    def handle_node_creation(self, value: List[Change]):
        # Create rows for the table
        rows = list({f"| {self._format_entity_labels(change.about_node)} |" for change in value})

        # Define the header for the table
        header = "| Term |"

        # Write the "Node Created" section as a markdown table
        self.write_markdown_table(f"Other nodes added: {len(rows)}", header, rows)

    def handle_class_creation(self, value: List[Change]):
        # Create rows for the table
        rows = list({f"| {self._format_entity_labels(change.about_node)} |" for change in value})

        # Define the header for the table
        header = "| Term |"

        # Write the "Class Created" section as a markdown table
        self.write_markdown_table(f"Classes added: {len(rows)}", header, rows)

    def handle_node_deletion(self, value: List[Change]):
        # Create rows for the table
        rows = list({f"| {self._format_entity_labels(change.about_node)} |" for change in value})

        # Define the header for the table
        header = "| Term |"

        # Write the "Nodes Deleted" section as a markdown table
        self.write_markdown_table(f"Nodes removed: {len(rows)}", header, rows)

    def handle_new_text_definition(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.new_value} |"
                for change in value
            }
        )
        header = "| Term | New Text Definition |"
        self.write_markdown_table(f"Text definitions added: {len(rows)}", header, rows)

    def handle_remove_text_definition(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.old_value} |"
                for change in value
            }
        )
        header = "| Term | Removed Text Definition |"
        self.write_markdown_table(f"Text definitions removed: {len(rows)}", header, rows)

    def handle_node_obsoletion_with_direct_replacement(self, value: List[Change]):
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} |\
                  {self._format_entity_labels(change.has_direct_replacement)} |"
                for change in value
            }
        )
        header = "| Term | Replacement |"
        self.write_markdown_table(f"Nodes obsoleted with replacement: {len(rows)}", header, rows)

    def handle_node_obsoletion(self, value: List[Change]):
        rows = [f"| {self._format_entity_labels(change.about_node)} |" for change in value]
        header = "| Term |"
        self.write_markdown_table(f"Nodes obsoleted without replacement: {len(rows)}", header, rows)

    def handle_node_direct_merge(self, value: List[Change]):
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} |\
                  {self._format_entity_labels(change.has_direct_replacement)} |"
                for change in value
            }
        )
        header = "| Term | Replacement |"
        self.write_markdown_table(f"Nodes merged: {len(rows)}", header, rows)

    def handle_add_node_to_subset(self, value: List[Change]):
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.in_subset} |"
                for change in value
            }
        )
        header = "| Term | Subset |"
        self.write_markdown_table(f"Nodes added to subset: {len(rows)}", header, rows)

    def handle_remove_node_from_subset(self, value: List[Change]):
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | {change.in_subset} |"
                for change in value
            }
        )
        header = "| Term | Subset |"
        self.write_markdown_table(f"Nodes removed from subset: {len(rows)}", header, rows)

    def handle_mapping_creation(self, value: List[Change]):
        rows = list(
            {
                f"""| {self._format_entity_labels(change.subject)} | """
                f"""{change.predicate} | """
                f"""{self._format_entity_labels(change.object)} |"""
                for change in value
            }
        )

        header = "| Subject | Predicate | Object |"
        self.write_markdown_table(f"Mappings added: {len(rows)}", header, rows)

    def handle_mapping_predicate_change(self, value: List[Change]):
        # Create rows for the table
        rows = list(
            {
                f"| {self._format_entity_labels(change.about_node)} | \
                {self._format_entity_labels(change.old_value)} |\
                {self._format_entity_labels(change.new_value)} | \
                {self._format_entity_labels(change.object)} |"
                for change in value
            }
        )

        # Define the header for the table
        header = "| Subject | Old Mapping Predicate | New Mapping Predicate | Object |"

        # Write the "Predicate Changed" section as a collapsible markdown table
        self.write_markdown_table(f"Mappings changed: {len(rows)}", header, rows)

    def handle_remove_mapping(self, value: List[Change]):
        rows = list(
            {
                f"""| {self._format_entity_labels(change.about_node)} | """
                f"""{change.predicate} | """
                f"""{self._format_entity_labels(change.object)} |"""
                for change in value
            }
        )

        header = "| Subject | Predicate | Object |"
        self.write_markdown_table(f"Mappings removed: {len(rows)}", header, rows)

    # def handle_datatype_or_language_tag_change(self, value:List[Change]):
    #     # Implement datatype or language tag change handling logic here
    #     logging.info("Datatype or language tag change handling not yet implemented.")

    # def handle_language_tag_change(self, value:List[Change]):
    #     # Implement language tag change handling logic here
    #     logging.info("Language tag change handling not yet implemented.")

    # def handle_datatype_change(self, value:List[Change]):
    #     # Implement datatype change handling logic here
    #     logging.info("Datatype change handling not yet implemented.")

    # def handle_allows_automatic_replacement_of_edges(self, value:List[Change]):
    #     # Implement allows automatic replacement of edges handling logic here
    #     logging.info("Allows automatic replacement of edges handling not yet implemented.")

    # def handle_unobsoletion(self, value:List[Change]):
    #     # Implement unobsoletion handling logic here
    #     logging.info("Unobsoletion handling not yet implemented.")

    # def handle_deletion(self, value:List[Change]):
    #     # Implement deletion handling logic here
    #     logging.info("Deletion handling not yet implemented.")

    # def handle_creation(self, value:List[Change]):
    #     # Implement creation handling logic here
    #     logging.info("Creation handling not yet implemented.")

    # def handle_subset_membership_change(self, value:List[Change]):
    #     # Implement subset membership change handling logic here
    #     logging.info("Subset membership change handling not yet implemented.")

    # def handle_add_to_subset(self, value:List[Change]):
    #     # Implement add to subset handling logic here
    #     logging.info("Add to subset handling not yet implemented.")

    # def handle_remove_from_subset(self, value:List[Change]):
    #     # Implement remove from subset handling logic here
    #     logging.info("Remove from subset handling not yet implemented.")

    # def handle_place_under(self, value:List[Change]):
    #     # Implement place under handling logic here
    #     logging.info("Place under handling not yet implemented.")

    def process_changes(self, curie_or_change: Dict[str, Change]):
        # Write overview and summary at the beginning of the document
        # self.write_markdown_overview_and_summary(curie_or_change)
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
            "NewTextDefinition": self.handle_new_text_definition,  # ! same as NodeTextDefinition
            "RemoveTextDefinition": self.handle_remove_text_definition,
            "NodeObsoletionWithDirectReplacement": self.handle_node_obsoletion_with_direct_replacement,
            "NodeObsoletion": self.handle_node_obsoletion,
            "NodeDirectMerge": self.handle_node_direct_merge,
            "EdgeCreation": self.handle_edge_creation,
            "EdgeChange": self.handle_edge_change,
            "AddNodeToSubset": self.handle_add_node_to_subset,
            "RemoveNodeFromSubset": self.handle_remove_node_from_subset,
            "MappingPredicateChange": self.handle_mapping_predicate_change,
            "MappingCreation": self.handle_mapping_creation,
            "RemoveMapping": self.handle_remove_mapping,
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

    def _format_entity_labels(self, entity):
        if self.oi.label(entity):
            return f"{self.oi.label(entity)} ({entity})"
        else:
            return entity
