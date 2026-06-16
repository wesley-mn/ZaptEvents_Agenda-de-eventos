from datetime import date
from pathlib import Path
import pprint

from modelos.contratante import Contratante
from modelos.evento import Evento, formatar_reais
from dados.base_dados import EVENTOS


class Agenda:
    """
    Controla as regras do sistema: cadastro, consulta, edição, remoção,
    persistência dos dados e relatórios financeiros.
    """

    def __init__(self):
        self.eventos = []
        self._carregar_base()
        self.proximo_id = max((evento.evento_id for evento in self.eventos), default=0) + 1

    # Converte as tuplas da base em objetos para uso durante a execução.
    def _carregar_base(self):
        for registro in EVENTOS:
            (
                evento_id,
                nome,
                dia,
                mes,
                ano,
                data_formatada,
                horario,
                local,
                quantidade,
                dados_contratante,
                itens_custo,
            ) = registro

            nome_contratante, tipo_documento, documento, whatsapp = dados_contratante

            contratante = Contratante(
                nome_contratante,
                tipo_documento,
                documento,
                whatsapp,
            )

            self.eventos.append(
                Evento(
                    evento_id,
                    nome,
                    dia,
                    mes,
                    ano,
                    data_formatada,
                    horario,
                    local,
                    quantidade,
                    contratante,
                    itens_custo,
                )
            )

    # Atualiza o arquivo dados/base_dados.py após alterações.
    # Assim, as mudanças continuam salvas mesmo depois que o programa fecha.
    def _salvar_base(self):
        registros = []

        for evento in self.eventos:
            registros.append(
                (
                    evento.evento_id,
                    evento.nome,
                    evento.dia,
                    evento.mes,
                    evento.ano,
                    evento.data_formatada,
                    evento.horario,
                    evento.local,
                    evento.quantidade_pessoas,
                    (
                        evento.contratante.nome,
                        evento.contratante.tipo_documento,
                        evento.contratante.documento,
                        evento.contratante.whatsapp,
                    ),
                    tuple(evento.itens_custo),
                )
            )

        caminho = Path(__file__).resolve().parent / "dados" / "base_dados.py"

        conteudo = (
            "# Banco de dados interno em Python.\n"
            "# Cada evento é representado por uma tupla.\n"
            "# O sistema atualiza este arquivo automaticamente ao cadastrar, editar ou remover dados.\n\n"
            "EVENTOS = "
            + pprint.pformat(registros, width=120, sort_dicts=False)
            + "\n"
        )

        caminho.write_text(conteudo, encoding="utf-8")

    def _buscar_por_id(self, evento_id):
        for evento in self.eventos:
            if evento.evento_id == evento_id:
                return evento
        return None

    def _data_ocupada(self, dia, mes, ano, ignorar_id=None):
        for evento in self.eventos:
            if ignorar_id is not None and evento.evento_id == ignorar_id:
                continue
            if evento.dia == dia and evento.mes == mes and evento.ano == ano:
                return evento
        return None

    def _pedir_texto(self, mensagem):
        while True:
            texto = input(mensagem).strip()
            if texto:
                return texto
            print("\n⚠️ Este campo não pode ficar vazio.")

    def _pedir_inteiro_positivo(self, mensagem):
        while True:
            try:
                valor = int(input(mensagem))
            except ValueError:
                print("\n⚠️ Digite apenas números inteiros.")
                continue

            if valor < 1:
                print("\n⚠️ Digite um número maior que zero.")
                continue

            return valor

    def _pedir_id(self):
        try:
            return int(input("\nDigite o código do evento: ").strip())
        except ValueError:
            print("\n⚠️ Digite apenas números.")
            return None

    def _pedir_data(self, ignorar_id=None):
        while True:
            try:
                dia = int(input("Dia: "))
                mes = int(input("Mês: "))
                ano = int(input("Ano: "))
                date(ano, mes, dia)
            except ValueError:
                print("\n⚠️ Data inválida. Tente novamente.")
                continue

            if ano < 2026 or ano > 2100:
                print("\n⚠️ Digite um ano entre 2026 e 2100.")
                continue

            conflito = self._data_ocupada(dia, mes, ano, ignorar_id)
            if conflito:
                print("\n❌ Já existe um evento nessa data: {}.".format(conflito.nome))
                continue

            return dia, mes, ano

    def _pedir_horario(self):
        while True:
            horario = input("Horário (HH:MM): ").strip()

            if len(horario) != 5 or horario[2] != ":":
                print("\n⚠️ Use o formato HH:MM. Exemplo: 14:30.")
                continue

            hora, minuto = horario.split(":")

            if not hora.isdigit() or not minuto.isdigit():
                print("\n⚠️ Digite apenas números no horário.")
                continue

            if not 0 <= int(hora) <= 23 or not 0 <= int(minuto) <= 59:
                print("\n⚠️ Horário inválido.")
                continue

            return horario

    def _pedir_documento(self):
        while True:
            tipo = input("Tipo de documento (CPF ou CNPJ): ").strip().upper()

            if tipo not in ("CPF", "CNPJ"):
                print("\n⚠️ Digite CPF ou CNPJ.")
                continue

            documento = input("Número do documento: ").strip()
            tamanho = 11 if tipo == "CPF" else 14

            if not documento.isdigit() or len(documento) != tamanho:
                print("\n⚠️ {} deve possuir exatamente {} números.".format(tipo, tamanho))
                continue

            return tipo, documento

    def _pedir_whatsapp(self):
        while True:
            numero = input("WhatsApp com DDD (11 números): ").strip()

            if numero.isdigit() and len(numero) == 11:
                return numero

            print("\n⚠️ WhatsApp inválido. Digite exatamente 11 números.")

    def _pedir_valor(self):
        while True:
            entrada = input("Valor: R$ ").strip().replace(",", ".")

            try:
                valor = float(entrada)
            except ValueError:
                print("\n⚠️ Digite um valor numérico válido.")
                continue

            if valor <= 0:
                print("\n⚠️ O valor deve ser maior que zero.")
                continue

            return valor

    def _pedir_resposta_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "n"):
                return resposta
            print("\n⚠️ Digite apenas s ou n.")

    def cadastrar_evento(self):
        print("\n── Cadastro do Evento ──")

        nome = self._pedir_texto("Nome do evento: ")
        dia, mes, ano = self._pedir_data()
        horario = self._pedir_horario()
        local = self._pedir_texto("Local: ")
        quantidade = self._pedir_inteiro_positivo("Quantidade de pessoas: ")

        print("\n── Dados do Contratante ──")

        nome_contratante = self._pedir_texto("Nome do contratante: ")
        tipo_documento, documento = self._pedir_documento()
        whatsapp = self._pedir_whatsapp()

        contratante = Contratante(
            nome_contratante,
            tipo_documento,
            documento,
            whatsapp,
        )

        evento = Evento(
            self.proximo_id,
            nome,
            dia,
            mes,
            ano,
            "{}-{:02d}-{:02d}".format(ano, mes, dia),
            horario,
            local,
            quantidade,
            contratante,
            [],
        )

        while self._pedir_resposta_sim_nao("\nAdicionar item de custo? (s/n): ") == "s":
            nome_item = self._pedir_texto("Nome do custo: ")
            valor = self._pedir_valor()
            evento.adicionar_item_custo(nome_item, valor)

        self.eventos.append(evento)
        self.proximo_id += 1
        self._salvar_base()

        print("\n✅ Evento cadastrado e salvo!")
        print("🆔 Código: {}".format(evento.evento_id))

    def listar_eventos(self):
        if not self.eventos:
            print("\nNenhum evento cadastrado.")
            return

        print("\n══════ LISTA DE EVENTOS ══════")
        for evento in self.eventos:
            evento.exibir_dados()

    def consultar_evento(self):
        evento_id = self._pedir_id()
        if evento_id is None:
            return

        evento = self._buscar_por_id(evento_id)

        if evento:
            evento.exibir_dados()
        else:
            print("\n❌ Evento não encontrado.")

    def editar_evento(self):
        evento_id = self._pedir_id()
        if evento_id is None:
            return

        evento = self._buscar_por_id(evento_id)

        if not evento:
            print("\n❌ Evento não encontrado.")
            return

        while True:
            evento.exibir_dados()

            print("\nO que deseja editar?")
            print("1. Nome")
            print("2. Data")
            print("3. Horário")
            print("4. Local")
            print("5. Quantidade de pessoas")
            print("6. Dados do contratante")
            print("0. Concluir")

            opcao = input("Escolha: ").strip()

            if opcao == "1":
                evento.nome = self._pedir_texto("Novo nome: ")
            elif opcao == "2":
                dia, mes, ano = self._pedir_data(evento.evento_id)
                evento.dia = dia
                evento.mes = mes
                evento.ano = ano
                evento.data_formatada = "{}-{:02d}-{:02d}".format(ano, mes, dia)
            elif opcao == "3":
                evento.horario = self._pedir_horario()
            elif opcao == "4":
                evento.local = self._pedir_texto("Novo local: ")
            elif opcao == "5":
                evento.quantidade_pessoas = self._pedir_inteiro_positivo("Nova quantidade: ")
            elif opcao == "6":
                evento.contratante.nome = self._pedir_texto("Novo nome do contratante: ")
                (
                    evento.contratante.tipo_documento,
                    evento.contratante.documento,
                ) = self._pedir_documento()
                evento.contratante.whatsapp = self._pedir_whatsapp()
            elif opcao == "0":
                print("\n✅ Edição concluída.")
                return
            else:
                print("\n⚠️ Opção inválida.")
                continue

            self._salvar_base()
            print("\n✅ Alteração salva na base.")

    def remover_evento(self):
        evento_id = self._pedir_id()
        if evento_id is None:
            return

        evento = self._buscar_por_id(evento_id)

        if not evento:
            print("\n❌ Evento não encontrado.")
            return

        evento.exibir_dados()
        confirmacao = self._pedir_resposta_sim_nao("\nTem certeza que deseja remover? (s/n): ")

        if confirmacao == "n":
            print("\nRemoção cancelada.")
            return

        self.eventos.remove(evento)
        self._salvar_base()

        print("\n✅ Evento removido da base.")

    def gerenciar_custos(self):
        evento_id = self._pedir_id()
        if evento_id is None:
            return

        evento = self._buscar_por_id(evento_id)

        if not evento:
            print("\n❌ Evento não encontrado.")
            return

        while True:
            evento.exibir_dados()
            print("\nGerenciar custos:")
            print("1. Adicionar custo")
            print("2. Editar custo")
            print("3. Remover custo")
            print("0. Voltar")

            opcao = input("Escolha: ").strip()

            if opcao == "1":
                nome = self._pedir_texto("Nome do custo: ")
                valor = self._pedir_valor()
                evento.adicionar_item_custo(nome, valor)
                self._salvar_base()
                print("\n✅ Custo adicionado e salvo.")

            elif opcao == "2":
                if not evento.itens_custo:
                    print("\n⚠️ Não existem custos cadastrados.")
                    continue

                indice = self._pedir_inteiro_positivo("Número do custo que deseja editar: ") - 1

                if indice < 0 or indice >= len(evento.itens_custo):
                    print("\n⚠️ Número de custo inválido.")
                    continue

                nome = self._pedir_texto("Novo nome do custo: ")
                valor = self._pedir_valor()
                evento.editar_item_custo(indice, nome, valor)
                self._salvar_base()
                print("\n✅ Custo editado e salvo.")

            elif opcao == "3":
                if not evento.itens_custo:
                    print("\n⚠️ Não existem custos cadastrados.")
                    continue

                indice = self._pedir_inteiro_positivo("Número do custo que deseja remover: ") - 1

                if indice < 0 or indice >= len(evento.itens_custo):
                    print("\n⚠️ Número de custo inválido.")
                    continue

                confirmacao = self._pedir_resposta_sim_nao("Confirmar remoção do custo? (s/n): ")

                if confirmacao == "s":
                    evento.remover_item_custo(indice)
                    self._salvar_base()
                    print("\n✅ Custo removido e salvo.")
                else:
                    print("\nRemoção cancelada.")

            elif opcao == "0":
                return

            else:
                print("\n⚠️ Opção inválida.")

    def resumo_financeiro(self):
        if not self.eventos:
            print("\nNenhum evento cadastrado.")
            return

        total = sum(evento.calcular_total() for evento in self.eventos)
        media = total / len(self.eventos)
        mais_caro = max(self.eventos, key=lambda evento: evento.calcular_total())
        mais_barato = min(self.eventos, key=lambda evento: evento.calcular_total())

        print("\n══════ RESUMO FINANCEIRO GERAL ══════")
        print("Eventos cadastrados: {}".format(len(self.eventos)))
        print("Total movimentado: {}".format(formatar_reais(total)))
        print("Média por evento: {}".format(formatar_reais(media)))
        print("Evento mais caro: {} - {}".format(
            mais_caro.nome,
            formatar_reais(mais_caro.calcular_total()),
        ))
        print("Evento mais barato: {} - {}".format(
            mais_barato.nome,
            formatar_reais(mais_barato.calcular_total()),
        ))

    def relatorio_mensal(self):
        while True:
            try:
                mes = int(input("Mês (1-12): "))
                ano = int(input("Ano: "))
            except ValueError:
                print("\n⚠️ Digite apenas números.")
                continue

            if not 1 <= mes <= 12:
                print("\n⚠️ Mês inválido.")
                continue

            break

        filtrados = [
            evento for evento in self.eventos
            if evento.mes == mes and evento.ano == ano
        ]

        if not filtrados:
            print("\nNenhum evento encontrado nesse período.")
            return

        total = sum(evento.calcular_total() for evento in filtrados)
        media = total / len(filtrados)
        mais_caro = max(filtrados, key=lambda evento: evento.calcular_total())

        print("\n══════ RELATÓRIO FINANCEIRO {:02d}/{} ══════".format(mes, ano))
        print("Eventos: {}".format(len(filtrados)))
        print("Total movimentado: {}".format(formatar_reais(total)))
        print("Média por evento: {}".format(formatar_reais(media)))
        print("Evento mais caro: {} - {}".format(
            mais_caro.nome,
            formatar_reais(mais_caro.calcular_total()),
        ))

    def gerar_relatorio_txt(self):
        if not self.eventos:
            print("\nNão existem eventos para gerar o relatório.")
            return

        caminho = Path(__file__).resolve().parent / "relatorios" / "relatorio_eventos.txt"

        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write("RELATÓRIO GERAL DE EVENTOS\n")
            arquivo.write("=" * 60 + "\n\n")

            for evento in self.eventos:
                arquivo.write("CÓDIGO: {}\n".format(evento.evento_id))
                arquivo.write("EVENTO: {}\n".format(evento.nome))
                arquivo.write("DATA: {} às {}\n".format(evento.data_formatada, evento.horario))
                arquivo.write("LOCAL: {}\n".format(evento.local))
                arquivo.write("PÚBLICO: {} pessoas\n".format(evento.quantidade_pessoas))
                arquivo.write("CONTRATANTE: {}\n".format(evento.contratante.nome))
                arquivo.write("{}: {}\n".format(
                    evento.contratante.tipo_documento,
                    evento.contratante.documento,
                ))
                arquivo.write("WHATSAPP: {}\n".format(evento.contratante.whatsapp))
                arquivo.write("CUSTOS:\n")

                if not evento.itens_custo:
                    arquivo.write("- Nenhum custo cadastrado.\n")
                else:
                    for nome, valor in evento.itens_custo:
                        arquivo.write("- {}: {}\n".format(nome, formatar_reais(valor)))

                arquivo.write("TOTAL: {}\n".format(formatar_reais(evento.calcular_total())))
                arquivo.write("-" * 60 + "\n\n")

            total = sum(evento.calcular_total() for evento in self.eventos)
            media = total / len(self.eventos)
            mais_caro = max(self.eventos, key=lambda evento: evento.calcular_total())
            mais_barato = min(self.eventos, key=lambda evento: evento.calcular_total())

            arquivo.write("RESUMO FINANCEIRO\n")
            arquivo.write("=" * 60 + "\n")
            arquivo.write("Total de eventos: {}\n".format(len(self.eventos)))
            arquivo.write("Total movimentado: {}\n".format(formatar_reais(total)))
            arquivo.write("Média por evento: {}\n".format(formatar_reais(media)))
            arquivo.write("Evento mais caro: {} - {}\n".format(
                mais_caro.nome,
                formatar_reais(mais_caro.calcular_total()),
            ))
            arquivo.write("Evento mais barato: {} - {}\n".format(
                mais_barato.nome,
                formatar_reais(mais_barato.calcular_total()),
            ))

        print("\n✅ Relatório criado em relatorios/relatorio_eventos.txt")
