# Transparência sobre uso de IA

Este arquivo foi incluído para atender à regra de transparência do desafio técnico.

## Ferramenta utilizada

- ChatGPT

## Objetivo do uso

A IA foi utilizada como apoio para acelerar a estruturação inicial do projeto, sugerir organização de pastas, gerar uma primeira versão do código, criar exemplos de README e propor ideias de diagnóstico de produtividade.

## Decisões humanas aplicadas

- Escolha de FastAPI pela simplicidade e geração automática de documentação.
- Escolha de SQLite para manter persistência simples sem exigir infraestrutura externa.
- Inclusão de validações para `nivel_foco`, `tempo_minutos`, `comentario`, `categoria` e `tags`.
- Inclusão de uma lógica criativa de feedback com base em média de foco, tempo total, percentual de sessões em flow e palavras citadas nos comentários.

## Prompts usados como referência

1. "Crie uma API em Python para registrar nível de foco, tempo de sessão e comentário, com endpoint de diagnóstico de produtividade."
2. "Organize o projeto com FastAPI, SQLite, README, validação de erros e testes simples."
3. "Inclua um arquivo explicando de forma transparente como a IA foi utilizada no projeto."

## Observação

O código deve ser revisado, executado localmente e ajustado conforme necessidade antes da entrega final.
