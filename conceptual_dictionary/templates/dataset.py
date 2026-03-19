dataset_template = {
    # dcat:Dataset — the dataset node
    "identifier": None,  # URI/IRI for the dataset, e.g. "https://doi.org/10.5281/zenodo.1234567"
    "title": None,  # dcterms:title, e.g. "Grain boundary energies for Al"
    # dcterms:creator — list of foaf:Person entries
    "creators": [
        {
            "id": None,  # URI for the person, e.g. "https://orcid.org/0000-0000-0000-0000"
            "name": None,  # foaf:name, e.g. "Abril Guzman"
        }
    ],
    # dcterms:isReferencedBy — the associated publication
    "publication": {
        "id": None,  # URI for the paper
        "identifier": None,  # dcterms:identifier — DOI string, e.g. "10.1016/j.actamat.2024.12345"
        "title": None,  # dcterms:title (optional)
    },
    # dcterms:isPartOf — list of sample IDs that belong to this dataset
    # (these are added as triples on each sample: sample dcterms:isPartOf dataset)
    "samples": [],
}
