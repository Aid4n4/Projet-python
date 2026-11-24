from Document import Document, HackerNewsDocument, ArxivDocument

class DocumentFactory:

    @staticmethod
    def creer_document(type_document, **kwargs):

        if type_document == "HackerNews":
            return HackerNewsDocument(**kwargs)

        elif type_document == "Arxiv":
            return ArxivDocument(**kwargs)

        else:
            return Document(**kwargs)