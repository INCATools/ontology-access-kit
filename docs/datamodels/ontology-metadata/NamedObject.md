# Class: NamedObject




URI: [omoschema:NamedObject](http://purl.obolibrary.org/obo/schema/NamedObject)




## Inheritance

* [Thing](Thing.md)
    * **NamedObject**
        * [Ontology](Ontology.md)
        * [Term](Term.md) [ HasSynonyms HasLifeCycle HasProvenance HasMappings HasCategory HasUserInformation HasMinimalMetadata]




## Slots

| Name | Range | Cardinality | Description  | Info |
| ---  | --- | --- | --- | --- |
| [id](id.md) | [uriorcurie](uriorcurie.md) | 1..1 | this maps to the URI in RDF  | . |


## Usages



## Identifier and Mapping Information









## LinkML Specification

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: NamedObject
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Thing
slots:
- id

```
</details>

### Induced

<details>
```yaml
name: NamedObject
from_schema: http://purl.obolibrary.org/obo/omo/schema
is_a: Thing
attributes:
  id:
    name: id
    description: this maps to the URI in RDF
    from_schema: http://purl.obolibrary.org/obo/omo/schema
    is_a: core_property
    identifier: true
    alias: id
    owner: NamedObject
    range: uriorcurie
    required: true

```
</details>