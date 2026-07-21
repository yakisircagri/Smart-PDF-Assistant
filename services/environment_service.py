document_count = 0

def set_document_count(count : int):
    global document_count
    document_count = count

def get_document_count():
    return document_count

document_metadata = {
    "filename" : None,
    "page_count" : 0,
    "chunk_count" : 0,
}

def set_document_metadata(filename : str, page_count : int, chunk_count : int):

    global document_metadata

    document_metadata = {
        "filename" : filename,
        "page_count" : page_count,
        "chunk_count" : chunk_count,
    }

def get_document_metadata():
    return document_metadata