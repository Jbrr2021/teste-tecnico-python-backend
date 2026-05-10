# 🤖 Transparência sobre uso de Inteligência Artificial

Este arquivo foi incluído para atender à regra de transparência do desafio técnico, que permite o uso de ferramentas de Inteligência Artificial desde que os artefatos gerados sejam commitados junto ao repositório.

O objetivo deste documento é explicar de forma clara como a IA foi utilizada no desenvolvimento da API de Foco e Produtividade.

---

## 🧠 Ferramentas de IA utilizadas

Durante o desenvolvimento, foram utilizadas as seguintes ferramentas:

- ChatGPT
- GitHub Copilot no VSCode

---

## 🎯 Objetivo do uso da IA

As ferramentas de IA foram utilizadas como apoio para acelerar o fluxo de desenvolvimento, organizar melhor a estrutura do projeto e revisar a entrega antes do commit final.

A IA foi usada principalmente para:

- entender melhor os requisitos do desafio;
- planejar a estrutura inicial do backend;
- sugerir organização de pastas e arquivos;
- gerar uma primeira base da API com FastAPI;
- apoiar a criação dos schemas de validação;
- sugerir a lógica do diagnóstico de produtividade;
- revisar o README.md;
- criar e melhorar testes automatizados;
- auxiliar nos comandos de Git;
- apoiar a documentação da entrega;
- revisar mensagens de commit e entrega no LinkedIn.

---

## 🛠️ Como cada ferramenta foi utilizada

### ChatGPT

O ChatGPT foi utilizado principalmente para:

- interpretar as regras do desafio técnico;
- sugerir a estrutura inicial do projeto;
- criar uma primeira versão dos arquivos principais;
- apoiar a escrita do README.md;
- sugerir exemplos de testes manuais;
- organizar a explicação sobre o uso de IA;
- auxiliar na preparação da mensagem de entrega.

### GitHub Copilot

O GitHub Copilot foi utilizado dentro do VSCode para:

- revisar arquivos do projeto;
- sugerir ajustes em dependências;
- melhorar a cobertura de testes;
- verificar comandos de execução local;
- auxiliar no processo de commit;
- ajudar na configuração do remoto Git;
- apoiar o envio do projeto para o GitHub.

---

## 👤 Decisões humanas aplicadas

Apesar do uso de IA, as principais decisões do projeto foram revisadas e validadas manualmente.

Decisões aplicadas durante o desenvolvimento:

- escolha do FastAPI pela simplicidade e documentação automática em `/docs`;
- escolha do SQLite para manter persistência simples sem infraestrutura externa;
- manutenção de uma estrutura de projeto simples e organizada;
- inclusão de validações para entradas inválidas;
- inclusão dos campos extras `categoria`, `tags` e `data_registro`;
- criação de uma lógica de diagnóstico com feedback automático;
- inclusão de testes automatizados;
- validação manual dos endpoints pela documentação interativa;
- revisão final antes do commit e push para o GitHub.

---

## ✅ Validações realizadas manualmente

A API foi executada localmente com o comando:

```bash
uvicorn app.main:app --reload