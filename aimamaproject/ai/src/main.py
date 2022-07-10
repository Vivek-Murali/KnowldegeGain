import json
import ast


def mapsets(results:list):
    response:list=[]
    for _,idx in enumerate(results):
        Data:dict = {}
        Data['row'] = _
        Data['uuid']=idx.uuid
        Data['doi'] = idx.doi
        Data['coreId'] = idx.coreId
        Data['title'] = idx.title
        Data['oai'] = idx.oai
        Data['issn'] = idx.issn
        Data['downloadUrl'] = idx.downloadUrl
        Data['fullText'] = idx.fullText
        Data['publisher'] = idx.publisher
        Data['abstract'] = idx.abstract
        Data['datePublished']= idx.datePublished
        Data['dateUpdated'] = idx.dateUpdated
        Data['pdfHashValue'] = idx.pdfHashValue
        Data['year'] = idx.year
        Data['magId'] = idx.magId
        Data['urls'] = idx.urls
        Data['relations'] = idx.relations
        Data['authors'] = idx.authors
        Data['fullTextIdentifier']= idx.fullTextIdentifier
        Data['topics'] = idx.topics
        Data['subjects'] = idx.subjects
        Data['contributors'] = idx.contributors
        Data['identifiers'] = idx.identifiers
        Data['enrichments'] = ast.literal_eval(idx.enrichments)
        if idx.language:
            Data['language'] = {k:y for k,y in idx.language.items()}
        else:
            Data['language'] = None
        if idx.journals:
            journals = []
            for idy in idx.journals:
                journal = {}
                journal['identifiers'] = idy.identifiers
                journal['title'] = idy.title
                journals.append(journal)
            Data['journals'] = journals
        else:
            Data['journals'] = None
        response.append(Data)
    return response