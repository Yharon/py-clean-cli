---
name: "📝 Changelog"
about: "Keep your changelog up to date"
title: "[CHANGELOG] "
labels: "changelog"
assignees: ''
---

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

#### Fase 4 - Modular Execution Architecture

- Criado arquivo `scripts/__main__.py` com argumentos globais (--verbose, --version, --help)
- Implementado sistema de help contextual para CLI hierárquico  
- Adicionados exemplos de uso para execução modular de comandos
- Implementada geração dinâmica de opções globais usando fields(RootConfig)
- Criado sistema de descoberta automática de comandos via CLI().scan()
- Implementada execução modular em scripts/commands/deploy/release.py
- Criada função test_func como exemplo de comando executável
- Adicionado discovery dinâmico de funções (main, test_func)
- Implementado roteamento de comandos para funções específicas
- Criado help contextual para módulos individuais
- Adicionadas diretrizes específicas do projeto py-clean-cli para desenvolvimento Python
- Criada metodologia de debugging sistemático baseada em lições aprendidas (debugging-methodology.instructions.md)
- Expandido protocolo de comunicação para resolução de problemas complexos
- Documentadas convenções para módulos CLI (função main, decorators, estrutura enterprise)
- Adicionados padrões de testes de integração para frameworks CLI
- Adicionadas diretrizes de gerenciamento de cache Python e ambiente de desenvolvimento

#### Fases Anteriores (Foundation)

- Sistema de exceções hierárquico com CLIError como base
- Decoradores @argument e @option para definição de argumentos CLI
- Scanner de estrutura que descobre comandos baseado em pastas
- Sistema de contexto tipado com merge de dataclasses
- Integração completa entre field.metadata e argumentos CLI
- Utilitários de tipagem forte com make_dataclass
- Suporte completo a type hints para IDEs
- AST parsing para detecção robusta de funções main()
- Sistema de validação para decorators
- Contextos imutáveis (frozen dataclasses) para type safety
- Builder de ArgumentParser com suporte a hierarquia de subcomandos
- Executor de comandos com injeção de contexto tipado
- API pública através da classe CLI com configuração flexível
- Sistema de configuração avançado com CLIConfig
- Estrutura enterprise complexa para validação real-world
- Comandos funcionais de user management (create, list)
- Sistema de help contextual completo

### Fixed

#### Fase 4 - Modular Architecture

- Corrigida descoberta de comandos em scripts/__main__.py para usar scanning dinâmico da biblioteca py-clean-cli
- Removidos prints hardcoded, agora usa CLI().scan() para descobrir comandos automaticamente
- Implementado fallback robusto em caso de falha na descoberta dinâmica
- Removido hardcode das opções --verbose, --version, --help
- Integrado fields(RootConfig) para descoberta automática de argumentos
- Adicionado mapeamento inteligente para short options (-v, -h)

#### Fases Anteriores

- Corrigido carregamento de funções: agora procura por "main" em vez do nome do arquivo
- Corrigido tratamento de decorators: diferenciação entre @argument ('name') e @option ('names')
- Corrigido configuração de argumentos: required=True apenas para argumentos opcionais
- Corrigido imports de módulos enterprise: DatabaseConfig vs DatabaseArgs
- Corrigido pipeline de execução: comandos agora executam completamente via CLI
- Corrigido injeção de contexto: GlobalConfig + UserConfig funcionando

### Changed

#### Fase 4 - Architecture Evolution

- __BREAKING__: Mudança de arquitetura de CLI centralizado para execução modular
- __SPECIFICATION__: Clarificada especificação real do projeto (modular vs centralizado)
- __USAGE PATTERN__: Novo padrão py -m scripts.commands.module.file command function
- __HIERARCHY__: Implementada herança hierárquica de argumentos por nível de pasta
- Corrigido sistema de help: argumentos posicionais e opcionais exibidos corretamente

### Changed

- Reorganizada estrutura de documentação para pasta docs/context/
- Movido .gitignore para .config/.gitignore conforme padrão do projeto
- Reorganizado README.md para docs/README.md
- Atualizado pyproject.toml para nova localização do README
- Removidos arquivos de teste e demo temporários para limpeza do repositório
- Estrutura enterprise para testes real-world com múltiplos módulos
- Configurações de herança complexa (GlobalConfig, UserConfig, DatabaseConfig, DeployConfig)
- Comandos enterprise realistas (user management, database backup, deployment)
- Padrões avançados de decorators com tipos complexos (Optional, List, Literal)

### Changed

- Removida dependência obrigatória de BaseScriptArgs
- Qualquer dataclass pode ser usado como configuração
- Sistema de contexto reescrito para suporte a tipagem forte
- Scanner melhorado com fallback para parsing textual

### Fixed

- Autocomplete de IDEs agora funciona com contextos tipados
- Type checking estático totalmente funcional
- Validação de tipos em runtime
- Todos os problemas de type safety no módulo cli.py resolvidos
- Guards adequados para acesso a CommandInfo None
- Tratamento seguro de formatação de traceback
- Validação robusta de root_command antes da execução

### Issues Identificadas (Não Resolvidas)

- __Execução de comandos via python -m trava silenciosamente__: Comandos não executam quando chamados via module runner
- __Problemas de estrutura de módulos__: ImportError durante refactoring DefaultArgs → GlobalConfig
- __Gap de testes end-to-end__: Falta de validação de execução real de comandos
- __Module loading issues__: Estrutura scripts/commands/ pode não seguir convenções Python

## [1.0.0] - 2025-09-05

### Added

- Initial release
