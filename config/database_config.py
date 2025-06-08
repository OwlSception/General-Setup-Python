import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")  # Default to SQLite
DATABASE_URL = "sqlite:///test.db"
# DATABASE_URL = "postgresql://user:password@localhost/dogs"
# MONGO_URL = ""

pub_med_tags = {
    "AB": "Abstract",
    "AD": "Affiliation",
    "AID": "Article Identifier",
    "AIJ": "Authors",
    "DP": "Publication Date",
    "JID": "Journal ID",
    "LA": "Language",
    "PL": "Place of Publication",
    "PT": "Publication Type",
    "RN": "EC/RN number (e.g., enzyme commission number or chemical abstracts registry numbers)",
    "SO": "Source",
    "TA": "Journal Title Abbreviation",
    "TI": "Title",
    "VI": "Volume",
}

refseq_accn = {
    "NM_": "RefSeq mRNA in DNA format",
    "NR_": "RefSeq non-coding RNA",
    "NP_": "RefSeq protein",
    "NC_": "RefSeq genomic DNA: Complete genome or chromosome",
    "XP_": "Model RefSeq protein (not experimentally validated)",
    "XM_": "Model RefSeq mRNA (not experimentally validated)",
    "XR_": "Model RefSeq non-coding RNA (not experimentally validated)",
}
accn = {"NT": "Genomic Contig"}
# Dictionary of valid GenBank qualifiers
gen_bank_search_qualifiers = {
    "ACCN": "Accession number of the sequence record.",
    "ALL": "All fields: Contains all terms from all searchable database fields in the database.",
    "AUTH": "Author of the publication.",
    "BIOS": "BioSample ID for the sample.",
    "BPRJ": "BioProject ID associated with the record.",
    "CLON": "Clone name or identifier.",
    "COUN": "Country of sample origin.",
    "DATE": "Publication or update date.",
    "DEVS": "Developmental stage of the organism.",
    "ECNO": "EC number for enzymatic proteins.",
    "ENV": "Indicates if the sample is an environmental sample.",
    "FEAT": "Feature key (e.g., CDS, exon, gene).",
    "FKEY": "Feature key associated with the record.",
    "GENE": "Gene name or symbol.",
    "ISOL": "Isolate information.",
    "JOUR": "Journal where the sequence was published.",
    "KEYW": "Keyword in the sequence record or annotation.",
    "KYWD": "Keyword used for classification or annotation in the record.",
    "LENG": "Sequence length in base pairs.",
    "LOCN": "Geographic location (latitude and longitude).",
    "MDAT": "Modification date of the record.",
    "MOLWT": "Molecular weight of the sequence or product.",
    "MOLY": "Molecule type (e.g., mRNA, genomic DNA).",
    "ORGN": "Organism name (scientific or common name).",
    "PDAT": "Publication date of the record.",
    "PLAS": "Plasmid identifier.",
    "PROT": "Protein product of the sequence.",
    "PROP": "Properties of the sequence or product.",
    "SLEN": "Sequence length in base pairs.",
    "SQID": "Sequence identifier.",
    "STRA": "Strain of the organism.",
    "SUBS": "Subcellular location of the gene product.",
    "TAXN": "Taxonomic identifier.",
    "TISS": "Tissue type where the sample originated.",
    "TITL": "Title of the associated publication.",
    "WORD": "General keyword search across all fields.",
}

enembl_stable_identifier_prefixes = {
    "E": "exon",
    "FM": "protein family",
    "G": "gene",
    "GT": "gene tree",
    "P": "protein",
    "R": "regulatory feature",
    "T": "transcript",
}


def build_genbank_query(filters):
    """
    Build a GenBank query using standard qualifiers.

    Args:
        filters (dict): Dictionary of search filters where keys are qualifiers and values are criteria.

    Returns:
        str: A formatted query string for GenBank searches.
    """
    query_parts = []
    for key, value in filters.items():
        if key in gen_bank_search_qualifiers:
            query_parts.append(f"{key}:{value}")
        else:
            raise ValueError(
                f"Invalid qualifier: {key}. Refer to gen_bank_search_qualifiers for valid keys."
            )
    return " AND ".join(query_parts)
