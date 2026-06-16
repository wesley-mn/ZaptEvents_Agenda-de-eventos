class Contratante:
    """
    Representa a pessoa física ou empresa responsável por contratar um evento.
    """

    def __init__(self, nome, tipo_documento, documento, whatsapp):
        self.nome = nome
        self.tipo_documento = tipo_documento
        self.documento = documento
        self.whatsapp = whatsapp

    def exibir_dados(self):
        print("🏢 Contratante: {}".format(self.nome))
        print("📄 {}: {}".format(self.tipo_documento, self.documento))
        print("📱 WhatsApp: {}".format(self.whatsapp))
