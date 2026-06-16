# Sistema de Gestão de Eventos

## 1. Visão geral

Este projeto foi desenvolvido em Python para organizar eventos, contratantes e custos financeiros.

O sistema resolve um problema comum de empresas e profissionais que precisam controlar eventos manualmente. Ele permite cadastrar, consultar, editar e remover eventos, além de calcular valores em reais e gerar relatórios.

## 2. Estrutura do projeto

```text
projeto_eventos_final/
├── main.py
├── agenda.py
├── testar_sistema.py
├── modelos/
│   ├── contratante.py
│   └── evento.py
├── dados/
│   └── base_dados.py
├── relatorios/
└── README.md
```

## 3. Responsabilidade de cada arquivo

| Arquivo ou pasta | Responsabilidade |
|---|---|
| `main.py` | Exibe o menu principal |
| `agenda.py` | Controla cadastros, consultas, validações, edições, remoções e relatórios |
| `modelos/evento.py` | Representa cada evento e calcula os custos |
| `modelos/contratante.py` | Representa o responsável pelo evento |
| `dados/base_dados.py` | Armazena os registros em Python |
| `relatorios/` | Recebe o relatório em TXT |
| `testar_sistema.py` | Executa testes automáticos |

## 4. Estruturas de dados utilizadas

### Lista

A lista é utilizada para reunir vários eventos. Ela permite adicionar, editar e remover registros durante a execução.

### Tupla

A tupla é utilizada para estruturar cada registro armazenado no banco interno em Python.

Cada item financeiro também é representado por uma tupla:

```python
("Buffet", 8500.00)
```

## 5. Relações entre elementos

```text
Contratante 1 ───── N Evento
Evento      1 ───── N Item de custo
```

Classificação:

- Um contratante pode estar relacionado a vários eventos.
- Cada evento possui um contratante.
- Um evento pode possuir vários itens de custo.
- Cada item de custo pertence a um evento.

## 6. Banco de dados interno

A base fica em:

```text
dados/base_dados.py
```

Ela contém 100 eventos.

Exemplos:

- Casamento de Mariana e Lucas
- Congresso Paranaense de Tecnologia e Inovação
- Formatura de Engenharia de Software - Turma 2026
- Feira Gastronômica Sabores do Paraná

O sistema salva automaticamente nesse arquivo quando um evento é cadastrado, editado ou removido.

## 7. Valores monetários

Cada evento pode possuir itens como:

- buffet;
- banda;
- DJ;
- fotógrafo;
- aluguel do espaço;
- decoração;
- iluminação;
- segurança;
- limpeza;
- recepção.

O sistema soma os valores automaticamente e apresenta o total em reais.

## 8. Funcionalidades

1. Cadastrar evento.
2. Listar eventos.
3. Consultar evento pelo código.
4. Editar evento.
5. Remover evento.
6. Adicionar, editar e remover itens de custo.
7. Exibir resumo financeiro geral.
8. Exibir relatório financeiro mensal.
9. Gerar relatório completo em TXT.

## 9. Validações

O sistema valida:

- nome obrigatório;
- local obrigatório;
- data existente;
- conflito entre eventos na mesma data;
- horário no formato `HH:MM`;
- quantidade de pessoas maior que zero;
- CPF com 11 números;
- CNPJ com 14 números;
- WhatsApp com 11 números;
- valores financeiros maiores que zero;
- respostas de confirmação com `s` ou `n`.

## 10. Como executar

Abra o terminal dentro da pasta do projeto e rode:

```bash
python main.py
```

## 11. Como executar os testes

```bash
python testar_sistema.py
```

## 12. Evolução em relação ao projeto anterior

A versão inicial possuía cadastro, listagem, edição, remoção e relatório simples.

A nova versão adiciona:

- banco interno em Python;
- 100 registros;
- identificador único;
- persistência dos dados;
- itens de custo;
- valores em reais;
- resumo financeiro;
- relatório mensal;
- relatório TXT completo;
- validações mais rigorosas;
- teste automático.

## Integrantes da equipe

* Eduardo Oliveira da Silva
* Wesley Henrique de Matos Nascimento
* Alexandre Zampronne Zaccaron Rocha
* Vinícius Oliveira Prado
* Matheus Felipe Alves Ferreira