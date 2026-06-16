from agenda import Agenda


def menu():
    agenda = Agenda()

    while True:
        print("\n══════════════════════════════════════")
        print("SISTEMA DE GESTÃO DE EVENTOS")
        print("══════════════════════════════════════")
        print("1. Cadastrar evento")
        print("2. Listar eventos")
        print("3. Consultar evento pelo código")
        print("4. Editar evento")
        print("5. Remover evento")
        print("6. Gerenciar custos")
        print("7. Resumo financeiro geral")
        print("8. Relatório financeiro mensal")
        print("9. Gerar relatório TXT")
        print("0. Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            agenda.cadastrar_evento()
        elif opcao == "2":
            agenda.listar_eventos()
        elif opcao == "3":
            agenda.consultar_evento()
        elif opcao == "4":
            agenda.editar_evento()
        elif opcao == "5":
            agenda.remover_evento()
        elif opcao == "6":
            agenda.gerenciar_custos()
        elif opcao == "7":
            agenda.resumo_financeiro()
        elif opcao == "8":
            agenda.relatorio_mensal()
        elif opcao == "9":
            agenda.gerar_relatorio_txt()
        elif opcao == "0":
            print("\nSaindo do sistema.")
            break
        else:
            print("\n⚠️ Opção inválida.")


if __name__ == "__main__":
    menu()
