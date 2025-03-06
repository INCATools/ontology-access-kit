import logging
from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, List, Optional, Union

import click
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import EnumDefinition, PermissibleValue
from linkml_runtime.linkml_model.meta import (
    AnonymousEnumExpression,
    EnumExpression,
    SchemaDefinition,
)
from linkml_runtime.loaders import yaml_loader
from ruamel.yaml import YAML

from oaklib import get_adapter
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.search_datamodel import SearchProperty, SearchTermSyntax
from oaklib.datamodels.value_set_configuration import Resolver, ValueSetConfiguration
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import SearchInterface
from oaklib.interfaces.basic_ontology_interface import BasicOntologyInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE

DEFAULT_CONFIG = ValueSetConfiguration(default_resolver=Resolver("", shorthand_prefix="sqlite:obo"))

logger = logging.getLogger(__name__)


@dataclass
class ValueSetExpander(BasicOntologyInterface, ABC):
    """
    Tool for working with Value Sets in OAK
    """

    configuration: ValueSetConfiguration = field(default_factory=lambda: DEFAULT_CONFIG)

    def expand_value_set(
        self,
        value_set: Union[EnumDefinition, AnonymousEnumExpression],
        schema: SchemaDefinition = None,
        source_enum_definition: EnumDefinition = None,
        pv_syntax: Optional[str] = None,
    ) -> Iterator[PermissibleValue]:
        """
        Expand a value set definition into a list of curies

        See:

         - https://douroucouli.wordpress.com/2022/07/15/using-ontologies-within-data-models-and-standards/

        TODO: extend this to allow FHIR value sets

        :param value_set: a named enum or enum expression
        :param schema: the schema to which the enum belongs
        :param source_enum_definition: if empty, the value_set is assumed to be a named enum
        :return:
        """
        if isinstance(value_set, EnumDefinition):
            if source_enum_definition is None:
                source_enum_definition = value_set
        pvs = list(value_set.permissible_values.values())
        if value_set.inherits:
            if schema is None:
                raise ValueError("Schema must be provided to expand value set")
            for inherited in value_set.inherits:
                if inherited not in schema.enums:
                    raise ValueError(f"Unknown value set: {inherited}")
                vset = schema.enums[inherited]
                pvs.extend(
                    self.expand_value_set(
                        vset,
                        schema=schema,
                        source_enum_definition=source_enum_definition,
                        pv_syntax=pv_syntax,
                    )
                )
        if value_set.include:
            for include in value_set.include:
                if isinstance(include, AnonymousEnumExpression):
                    pvs.extend(
                        self.expand_value_set(
                            include,
                            schema=schema,
                            source_enum_definition=source_enum_definition,
                            pv_syntax=pv_syntax,
                        )
                    )
                else:
                    raise ValueError(f"Unexpected type for include: {type(include)}")
                pvs.extend(
                    self.expand_value_set(
                        include,
                        schema=schema,
                        source_enum_definition=source_enum_definition,
                        pv_syntax=pv_syntax,
                    )
                )
        if value_set.concepts:
            for concept in value_set.concepts:
                pvs.append(PermissibleValue(text=concept, meaning=concept))
        if value_set.matches:
            m = value_set.matches
            oi = self._get_handle(m.source_ontology)
            if m.identifier_pattern:
                if isinstance(oi, SearchInterface):
                    search_config = SearchConfiguration(
                        syntax=SearchTermSyntax.REGULAR_EXPRESSION,
                        properties=[SearchProperty.IDENTIFIER],
                    )
                    for curie in oi.basic_search(m.identifier_pattern, config=search_config):
                        pvs.append(PermissibleValue(text=curie, meaning=curie))
                else:
                    raise NotImplementedError(f"Must be a SearchInterface: {type(oi)}")
        if value_set.reachable_from:
            rq = value_set.reachable_from
            oi = self._get_handle(rq.source_ontology)
            predicates = rq.relationship_types or [IS_A]
            logging.debug(f"Predicates: {predicates}")
            if isinstance(oi, OboGraphInterface):
                if rq.traverse_up:
                    if rq.is_direct:
                        results = [
                            o
                            for _s, _p, o in oi.relationships(
                                rq.source_nodes, predicates=predicates
                            )
                        ]
                    else:
                        results = oi.ancestors(
                            rq.source_nodes, predicates=predicates, reflexive=rq.include_self
                        )
                else:
                    if rq.is_direct:
                        results = [
                            s
                            for s, _p, _o in oi.relationships(
                                objects=rq.source_nodes, predicates=predicates
                            )
                        ]
                    else:
                        results = oi.descendants(
                            rq.source_nodes, predicates=predicates, reflexive=rq.include_self
                        )
                for curie in results:
                    pvs.append(
                        self._generate_permissible_value(
                            curie, oi, source_enum_definition, pv_syntax=pv_syntax
                        )
                    )
            else:
                raise NotImplementedError(f"Must be an OboGraphInterface: {type(oi)}")
        if value_set.minus:
            for minus_vs in value_set.minus:
                if isinstance(minus_vs, EnumExpression) or isinstance(
                    minus_vs, AnonymousEnumExpression
                ):
                    for pv in self.expand_value_set(
                        minus_vs,
                        schema=schema,
                        source_enum_definition=source_enum_definition,
                        pv_syntax=pv_syntax,
                    ):
                        if pv in pvs:
                            pvs.remove(pv)
                else:
                    raise ValueError(f"Unexpected type for minus: {type(minus_vs)}")
        for pv in pvs:
            yield pv

    def _get_handle(self, ontology_id: CURIE) -> BasicOntologyInterface:
        prefix, local_name = ontology_id.split(":")
        prefix_lower = prefix.lower()
        config = self.configuration
        resolver = None
        if config.default_resolver:
            resolver = config.default_resolver
        if prefix_lower in config.prefix_resolvers:
            resolver = config.prefix_resolvers[prefix_lower]
        if ontology_id in config.resource_resolvers:
            resolver = config.resource_resolvers[ontology_id]
        if resolver:
            if resolver.shorthand_prefix:
                shorthand = f"{resolver.shorthand_prefix}:{local_name}"
            elif resolver.shorthand:
                shorthand = resolver.shorthand
            else:
                raise ValueError(f"Invalid resolver configuration: {resolver}")
            return get_adapter(shorthand)
        else:
            raise ValueError(f"Don't know how to resolve: {ontology_id}")

    def _generate_permissible_value(
        self,
        curie: CURIE,
        oi: BasicOntologyInterface,
        enum_definition: EnumDefinition = None,
        pv_syntax: Optional[str] = None,
    ) -> PermissibleValue:
        definition = oi.definition(curie)
        # \n can break some downstream tooling like LinkML's gen-pydantic (v1.6.6)
        if definition is not None:
            definition = definition.replace("\n", " ")
        label = oi.label(curie)
        pv_formula = enum_definition.pv_formula if enum_definition else None
        if pv_syntax is not None:
            text = pv_syntax.format(id=curie, label=label, definition=definition)
        elif str(pv_formula) == "CURIE":
            text = curie
        elif str(pv_formula) == "LABEL":
            # not all ontologies will have text for every element
            if label is not None:
                text = label
            else:
                text = curie
        elif str(pv_formula) == "URI":
            text = curie
        elif str(pv_formula) == "CODE":
            text = curie.split(":")[1]
        else:
            text = curie
        return PermissibleValue(text=text, meaning=curie, description=definition, title=label)

    def expand_in_place(
        self,
        schema_path: Union[str, Path],
        value_set_names: List[str] = None,
        output_path: Union[str, Path] = None,
        pv_syntax: Optional[str] = None,
    ) -> SchemaDefinition:
        """
        Expand value sets in place

        :param schema_path:
        :param value_set_names:
        :param configuration:
        :param output_path:
        :return:
        """
        yaml = YAML()
        with open(schema_path) as file:
            yaml_obj = yaml.load(file)
        from linkml_runtime.loaders import yaml_loader

        schema = yaml_loader.load(schema_path, target_class=SchemaDefinition)
        if value_set_names is None:
            value_set_names = list(schema.enums.keys())
        for value_set_name in value_set_names:
            if value_set_name not in schema.enums:
                raise ValueError(f"Unknown value set: {value_set_name}")
            value_set = schema.enums[value_set_name]
            pvs = list(self.expand_value_set(value_set, schema=schema, pv_syntax=pv_syntax))
            yaml_obj["enums"][value_set_name]["permissible_values"] = {
                str(pv.text): json_dumper.to_dict(pv) for pv in pvs
            }
        if output_path:
            with open(output_path, "w", encoding="UTF-8") as file:
                yaml.dump(yaml_obj, stream=file)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
def main(verbose: int, quiet: bool):
    """Run the ValueSet CLI."""
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command()
@click.option("-c", "--config", type=click.Path(exists=True))
@click.option("-s", "--schema", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path())
@click.option("--pv-syntax", help="Enter a LinkML structured_pattern.syntax-style string ")
# # add a boolean click option with --mixs-style and (default) --no-mixs-style options
# @click.option("-m", "--mixs-style", is_flag=True, default=False)
@click.argument("value_set_names", nargs=-1)
def expand(config: str, schema: str, value_set_names: List[str], output: str, pv_syntax: str):
    """
    Expand a value set. EXPERIMENTAL.

    This will expand an *intentional value set* (aka *dynamic enum*), running a query against
    an ontology backend or backends to materialize the value set (permissible values).

    Currently the value set must be specified as LinkML, but in future this will be
    possible with other specifications such as FHIR ValueSet objects.

    Each expression in a dynamic enum has a *source ontology*, this is specified as a CURIE
    such as:

    - obo:mondo
    - bioregistry:wikidata

    These can be mapped to specific OAK selectors. By default, any obo prefix is mapped to
    the semsql implementation of that. You can use a configuration file to map to other backends,
    such as BioPortal or Wikidata. However, note that not all backends are capable of being able to
    render all value sets.

    Examples:

        vskit expand -c config.yaml -s schema.yaml -o expanded.yaml my_value_set1 my_value_set2

    Custom permissible value syntax:

        vskit expand -s schema.yaml -o expanded.yaml --pv-syntax '{label} [{id}] my_value_set1

    For more examples, see:

       https://incatools.github.io/ontology-access-kit/examples/AdHoc/ValueSets.html

    """
    value_set_names = None if not value_set_names else value_set_names
    expander = ValueSetExpander()
    if config:
        expander.configuration = yaml_loader.load(config, target_class=ValueSetConfiguration)
    expander.expand_in_place(
        schema_path=schema, value_set_names=value_set_names, output_path=output, pv_syntax=pv_syntax
    )


if __name__ == "__main__":
    main()
