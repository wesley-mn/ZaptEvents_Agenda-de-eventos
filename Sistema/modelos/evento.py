def formatar_reais(valor):
    """
    Converte um número para o formato monetário brasileiro.
    Exemplo: 8500 vira R$ 8.500,00.
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Evento:
    """
    Representa um evento, seu contratante e os custos vinculados.
    """

    def __init__(
        self,
        evento_id,
        nome,
        dia,
        mes,
        ano,
        data_formatada,
        horario,
        local,
        quantidade_pessoas,
        contratante,
        itens_custo=None,
    ):
        self.evento_id = evento_id
        self.nome = nome
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.data_formatada = data_formatada
        self.horario = horario
        self.local = local
        self.quantidade_pessoas = quantidade_pessoas
        self.contratante = contratante
        self.itens_custo = list(itens_custo) if itens_custo is not None else []

    def adicionar_item_custo(self, nome, valor):
        """
        Armazena cada item financeiro como uma tupla: (nome, valor).
        """
        self.itens_custo.append((nome, valor))

    def editar_item_custo(self, indice, novo_nome, novo_valor):
        self.itens_custo[indice] = (novo_nome, novo_valor)

    def remover_item_custo(self, indice):
        self.itens_custo.pop(indice)

    def calcular_total(self):
        """
        Soma os valores de todos os itens financeiros do evento.
        """
        return sum(valor for nome, valor in self.itens_custo)

    def exibir_dados(self):
        print("\n────────────────────────────────────────")
        print("🆔 Código: {}".format(self.evento_id))
        print("🎉 Evento: {}".format(self.nome))
        print("📅 Data: {}".format(self.data_formatada))
        print("⌚ Horário: {}".format(self.horario))
        print("📍 Local: {}".format(self.local))
        print("👥 Pessoas: {}".format(self.quantidade_pessoas))
        self.contratante.exibir_dados()

        print("\n💰 Itens de custo:")
        if not self.itens_custo:
            print("- Nenhum custo cadastrado.")
        else:
            for numero, (nome, valor) in enumerate(self.itens_custo, start=1):
                print("{}. {}: {}".format(numero, nome, formatar_reais(valor)))

        print("💵 Total: {}".format(formatar_reais(self.calcular_total())))
        print("────────────────────────────────────────")
