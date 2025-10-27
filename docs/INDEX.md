# Documentação do Sistema# Documentation Index - Evacuation System



Índice geral da documentação do Sistema de Simulação e Otimização de Evacuação de Multidões.## 📚 Complete Documentation Guide



## 📚 Documentos PrincipaisThis index provides quick access to all documentation in the system.



### Para Usuários---



**[Guia do Usuário](USER_GUIDE.md)**  ## 🚀 Quick Start

Manual completo de uso da interface web. Inclui:

- Navegação pela interface**New to the project?** Start here:

- Criação e gestão de mapas

- Configuração de parâmetros1. [Project Overview](README_PROJETO.md) - High-level architecture and goals

- Execução de simulações e otimizações2. [Architecture Guide](ARCHITECTURE.md) - System design and patterns

- Análise e exportação de resultados3. [API Reference](API_REFERENCE.md) - Complete API documentation

- Solução de problemas comuns

**Want to use NSGA-II with cache?** Start here:

### Para Desenvolvedores

1. [NSGA Cached Quick Reference](NSGA_CACHED_QUICK_REFERENCE.md) - 3-step quick start

**[Arquitetura do Sistema](ARCHITECTURE.md)**  2. [NSGA Cached Integration Guide](NSGA_CACHED_INTEGRATION.md) - Complete documentation

Documentação técnica da arquitetura. Cobre:

- Visão geral e componentes**Want to create maps?** Start here:

- Fluxo de execução

- Estrutura de dados1. [Map Creation Guide](integration/map_creation_integration.md) - Complete guide

- Padrões de design utilizados2. [Map Creation Examples](integration/examples.md) - Practical examples



**[Guia de Desenvolvimento](DEVELOPMENT.md)**  ---

Orientações para desenvolvimento. Inclui:

- Estrutura do código## 📖 Documentation by Category

- APIs e integrações

- Como adicionar funcionalidades### System Architecture

- Testes automatizados

- Convenções de código| Document | Description | When to Read |

|----------|-------------|--------------|

**[Referência de API](API_REFERENCE.md)**  | [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture, patterns, data flows | Understanding system design |

Documentação detalhada das APIs internas. Abrange:| [API_REFERENCE.md](API_REFERENCE.md) | Complete API documentation | Using system APIs |

- Services de integração| [FILE_ROLES.md](FILE_ROLES.md) | Role and responsibility of each file | Finding specific functionality |

- Módulos do simulador| [SUMMARY.md](SUMMARY.md) | High-level project summary | Quick overview |

- Interfaces públicas

- Exemplos de uso### Integration Guides



### Configuração e Formato| Document | Description | When to Read |

|----------|-------------|--------------|

**[Formato de Configuração Unificada](UNIFIED_CONFIG_FORMAT.md)**  | [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) | **All integrations summary** | See all completed work |

Especificação do formato JSON de configuração. Detalha:| [INTEGRATION_REFACTOR_SUMMARY.md](INTEGRATION_REFACTOR_SUMMARY.md) | Integration API refactoring | Understanding integration layer |

- Estrutura de presets| [INTEGRATION_API_QUICK_REFERENCE.md](INTEGRATION_API_QUICK_REFERENCE.md) | Integration API quick reference | Using integration API |

- Parâmetros de algoritmos

- Parâmetros de simulação### NSGA-II Documentation

- Compatibilidade entre algoritmos

| Document | Description | When to Read |

## 🗂️ Organização da Documentação|----------|-------------|--------------|

| [NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md) | **⚡ Quick start (3 steps)** | Getting started quickly |

```| [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md) | **Complete integration guide** | Deep dive into cached NSGA-II |

docs/| [NSGA_3OBJECTIVE_MODE_GUIDE.md](NSGA_3OBJECTIVE_MODE_GUIDE.md) | **3-objective mode guide** | Optimizing iterations as objective |

├── INDEX.md                      # Este arquivo| [NSGA_CACHED_FINAL_SUMMARY.md](NSGA_CACHED_FINAL_SUMMARY.md) | Implementation summary | Understanding what was built |

├── USER_GUIDE.md                 # Guia do usuário completo

├── ARCHITECTURE.md               # Arquitetura do sistema### Map Creation

├── DEVELOPMENT.md                # Guia de desenvolvimento

├── API_REFERENCE.md              # Referência de APIs| Document | Description | When to Read |

└── UNIFIED_CONFIG_FORMAT.md      # Formato de configuração|----------|-------------|--------------|

```| [integration/map_creation_integration.md](integration/map_creation_integration.md) | Map creation integration guide | Using map editor |

| [integration/examples.md](integration/examples.md) | Practical examples | Learning by example |

## 🚀 Início Rápido| [integration/INTEGRATION_SUMMARY.md](integration/INTEGRATION_SUMMARY.md) | Map integration summary | Understanding map system |

| [integration/map_creation_changelog.md](integration/map_creation_changelog.md) | Detailed changelog | Tracking changes |

### Novos Usuários

### Interface Documentation

1. Leia o [README principal](../README.md) para visão geral

2. Execute `python setup_integration.py` para configurar| Document | Description | When to Read |

3. Consulte [Guia do Usuário](USER_GUIDE.md) para usar a interface|----------|-------------|--------------|

4. Veja exemplos em `presets/` para configurações prontas| [interface_docs/overview.md](interface_docs/overview.md) | Interface architecture overview | Understanding UI structure |

| [interface_docs/App.py.md](interface_docs/App.py.md) | Main app documentation | Understanding entry point |

### Novos Desenvolvedores| [interface_docs/SUMMARY.md](interface_docs/SUMMARY.md) | Interface summary | Quick interface overview |



1. Leia [Arquitetura](ARCHITECTURE.md) para entender o sistema### Configuration

2. Configure ambiente de desenvolvimento (veja [README](../README.md))

3. Consulte [Guia de Desenvolvimento](DEVELOPMENT.md) para padrões| Document | Description | When to Read |

4. Veja [API Reference](API_REFERENCE.md) para interfaces disponíveis|----------|-------------|--------------|

| [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md) | Unified configuration format spec | Creating config files |

## 📖 Documentação por Tópico| [examples/nsga_ii/README.md](../examples/nsga_ii/README.md) | NSGA-II config examples | NSGA-II configuration |



### Simulação### Project Management



- **Cellular Automata**: Ver [ARCHITECTURE.md - Core do Simulador](ARCHITECTURE.md#core-do-simulador)| Document | Description | When to Read |

- **Parâmetros de Simulação**: Ver [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md)|----------|-------------|--------------|

- **Execução**: Ver [USER_GUIDE.md - Execução](USER_GUIDE.md#execução-de-simulações)| [CHANGELOG_AUTOGERADO.md](CHANGELOG_AUTOGERADO.md) | Automated changelog | Tracking all changes |

| [RELATORIO_ERROS_ANALISE.md](RELATORIO_ERROS_ANALISE.md) | Error analysis report | Troubleshooting issues |

### Otimização

---

- **NSGA-II**: Ver [ARCHITECTURE.md - Fluxo NSGA-II](ARCHITECTURE.md#otimização-nsga-ii-pymoo)

- **Força Bruta**: Ver [USER_GUIDE.md - Força Bruta](USER_GUIDE.md#força-bruta)## 🎯 Documentation by Use Case

- **Configuração**: Ver [USER_GUIDE.md - Parâmetros](USER_GUIDE.md#configuração-de-parâmetros)

### "I want to run NSGA-II optimization faster"

### Mapas

1. **Quick Start:** [NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md)

- **Criação**: Ver [USER_GUIDE.md - Criação de Mapas](USER_GUIDE.md#criação-de-mapas)   - 3-step setup

- **Validação**: Ver [ARCHITECTURE.md - Módulo de Mapas](ARCHITECTURE.md#módulo-de-criação-de-mapas)   - When to use cached vs standard

- **Formatos**: Ver [DEVELOPMENT.md - Mapas](DEVELOPMENT.md#criação-de-mapas)   - Performance comparison



### Dados2. **Deep Dive:** [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md)

   - Architecture details

- **Banco de Dados**: Ver [ARCHITECTURE.md - SQLite](ARCHITECTURE.md#banco-de-dados-sqlite)   - API reference

- **Arquivos JSON**: Ver [ARCHITECTURE.md - JSON](ARCHITECTURE.md#arquivos-json)   - Troubleshooting

- **Exportação**: Ver [USER_GUIDE.md - Exportação](USER_GUIDE.md#exportação-de-dados)

3. **Examples:** [examples/nsga_ii/unified_config.json](../examples/nsga_ii/unified_config.json)

## 🔍 Encontrando Informações

### "I want to create evacuation maps"

### Por Tarefa

1. **Start Here:** [integration/map_creation_integration.md](integration/map_creation_integration.md)

| Quero... | Consulte... |   - Complete guide

|----------|-------------|   - Features overview

| Criar um mapa | [USER_GUIDE.md - Criação de Mapas](USER_GUIDE.md#criação-de-mapas) |   - Color scheme

| Executar simulação | [USER_GUIDE.md - Execução](USER_GUIDE.md#execução-de-simulações) |

| Configurar NSGA-II | [USER_GUIDE.md - Parâmetros](USER_GUIDE.md#configuração-de-parâmetros) |2. **Learn by Example:** [integration/examples.md](integration/examples.md)

| Analisar resultados | [USER_GUIDE.md - Análise](USER_GUIDE.md#análise-de-resultados) |   - Step-by-step examples

| Adicionar feature | [DEVELOPMENT.md - Funcionalidades](DEVELOPMENT.md#adicionando-funcionalidades) |   - Common patterns

| Entender arquitetura | [ARCHITECTURE.md](ARCHITECTURE.md) |

| Usar APIs internas | [API_REFERENCE.md](API_REFERENCE.md) |3. **Integration Details:** [integration/INTEGRATION_SUMMARY.md](integration/INTEGRATION_SUMMARY.md)

| Criar preset | [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md) |

### "I want to understand the system architecture"

### Por Componente

1. **High-Level:** [ARCHITECTURE.md](ARCHITECTURE.md)

| Componente | Documentação |   - System design

|------------|--------------|   - Design patterns

| Interface Streamlit | [ARCHITECTURE.md - Interface Web](ARCHITECTURE.md#interface-web-streamlit) |   - Data flows

| Services | [ARCHITECTURE.md - Integração](ARCHITECTURE.md#camada-de-integração-services) |

| Simulador | [ARCHITECTURE.md - Core](ARCHITECTURE.md#core-do-simulador) |2. **File Structure:** [FILE_ROLES.md](FILE_ROLES.md)

| Banco de Dados | [ARCHITECTURE.md - Armazenamento](ARCHITECTURE.md#armazenamento-de-dados) |   - What each file does

| NSGA-II | [ARCHITECTURE.md - NSGA-II](ARCHITECTURE.md#otimização-nsga-ii-pymoo) |   - Where to find functionality



## ❓ Perguntas Frequentes3. **API Details:** [API_REFERENCE.md](API_REFERENCE.md)

   - Complete API reference

**Como adiciono um novo algoritmo?**     - Usage examples

→ [DEVELOPMENT.md - Novo Algoritmo](DEVELOPMENT.md#novo-algoritmo-de-otimização)

### "I want to integrate a new module"

**Como funciona o sistema de presets?**  

→ [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md)1. **See What's Been Done:** [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)

   - All completed integrations

**Onde estão armazenados os resultados?**     - Patterns used

→ [ARCHITECTURE.md - Armazenamento](ARCHITECTURE.md#armazenamento-de-dados)   - Best practices



**Como debugar uma simulação que falha?**  2. **Integration Layer:** [INTEGRATION_REFACTOR_SUMMARY.md](INTEGRATION_REFACTOR_SUMMARY.md)

→ [USER_GUIDE.md - Solução de Problemas](USER_GUIDE.md#solução-de-problemas)   - How to use integration API

   - Avoiding code duplication

**Como rodar testes?**  

→ [DEVELOPMENT.md - Testes](DEVELOPMENT.md#testes)3. **Quick Reference:** [INTEGRATION_API_QUICK_REFERENCE.md](INTEGRATION_API_QUICK_REFERENCE.md)



## 📝 Convenções da Documentação### "I want to contribute to the project"



- **Código inline**: `código` ou `arquivo.py`1. **Project Overview:** [README_PROJETO.md](README_PROJETO.md)

- **Blocos de código**: Sempre com linguagem especificada2. **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)

- **Comandos shell**: Prefixados com `$` ou sem prefixo3. **Recent Changes:** [CHANGELOG_AUTOGERADO.md](CHANGELOG_AUTOGERADO.md)

- **Arquivos**: Caminhos relativos à raiz do projeto4. **Integration Examples:** [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)

- **Links**: Sempre relativos entre documentos

---

## 🔄 Atualizações

## 📝 Document Formats

Esta documentação é mantida sincronizada com o código. Última atualização: **Outubro 2024**

### Quick References (⚡ 5-10 min read)

Para contribuir com a documentação:

1. Siga o mesmo formato dos documentos existentesThese provide essential information fast:

2. Mantenha clareza e concisão- [NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md)

3. Adicione exemplos quando relevante- [INTEGRATION_API_QUICK_REFERENCE.md](INTEGRATION_API_QUICK_REFERENCE.md)

4. Atualize este INDEX se criar novos documentos- [SUMMARY.md](SUMMARY.md)



---### Complete Guides (📖 30-60 min read)



**Versão da Documentação:** 1.0  These provide comprehensive documentation:

**Sistema:** v1.0.0  - [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md)

**Data:** Outubro 2024- [ARCHITECTURE.md](ARCHITECTURE.md)

- [integration/map_creation_integration.md](integration/map_creation_integration.md)

### Summaries (📊 10-15 min read)

These provide overview and status:
- [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)
- [NSGA_CACHED_FINAL_SUMMARY.md](NSGA_CACHED_FINAL_SUMMARY.md)
- [integration/INTEGRATION_SUMMARY.md](integration/INTEGRATION_SUMMARY.md)

### References (🔍 Look up as needed)

These are for specific information:
- [API_REFERENCE.md](API_REFERENCE.md)
- [FILE_ROLES.md](FILE_ROLES.md)
- [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md)

---

## 🔗 Common Paths

### For Developers

```
Start: README_PROJETO.md
    ↓
ARCHITECTURE.md (understand design)
    ↓
INTEGRATION_STATUS.md (see what's built)
    ↓
API_REFERENCE.md (use APIs)
```

### For Users (NSGA-II)

```
Start: NSGA_CACHED_QUICK_REFERENCE.md
    ↓
Try it out (3 steps)
    ↓
NSGA_CACHED_INTEGRATION.md (if needed)
```

### For Users (Map Creation)

```
Start: integration/map_creation_integration.md
    ↓
integration/examples.md (learn patterns)
    ↓
Try it in interface
```

### For New Contributors

```
Start: README_PROJETO.md
    ↓
ARCHITECTURE.md
    ↓
INTEGRATION_STATUS.md (see integration patterns)
    ↓
Pick a module to work on
```

---

## 📦 Documentation Organization

```
docs/
├── INDEX.md (this file)                     ← You are here
│
├── Quick Starts
│   ├── NSGA_CACHED_QUICK_REFERENCE.md       ⚡ NSGA-II cached (3 steps)
│   └── INTEGRATION_API_QUICK_REFERENCE.md   ⚡ Integration API
│
├── Complete Guides
│   ├── NSGA_CACHED_INTEGRATION.md           📖 NSGA-II cached (full)
│   ├── ARCHITECTURE.md                      📖 System architecture
│   └── API_REFERENCE.md                     📖 API documentation
│
├── Summaries
│   ├── INTEGRATION_STATUS.md                📊 All integrations
│   ├── NSGA_CACHED_FINAL_SUMMARY.md         📊 NSGA-II summary
│   ├── INTEGRATION_REFACTOR_SUMMARY.md      📊 Refactor summary
│   └── SUMMARY.md                           📊 Project summary
│
├── References
│   ├── FILE_ROLES.md                        🔍 File reference
│   ├── UNIFIED_CONFIG_FORMAT.md             🔍 Config format
│   └── CHANGELOG_AUTOGERADO.md              🔍 Changelog
│
├── integration/                              Map creation docs
│   ├── map_creation_integration.md          📖 Complete guide
│   ├── examples.md                          📖 Examples
│   ├── INTEGRATION_SUMMARY.md               📊 Summary
│   └── ...
│
└── interface_docs/                           Interface docs
    ├── overview.md                          📖 UI architecture
    ├── App.py.md                            📖 App entry point
    └── ...
```

---

## 🎓 Learning Paths

### Path 1: Quick User (30 min)

1. [SUMMARY.md](SUMMARY.md) - 5 min
2. [NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md) - 10 min
3. [integration/examples.md](integration/examples.md) - 15 min
4. **Start using the system!**

### Path 2: Power User (2 hours)

1. [README_PROJETO.md](README_PROJETO.md) - 15 min
2. [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md) - 45 min
3. [integration/map_creation_integration.md](integration/map_creation_integration.md) - 30 min
4. [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md) - 15 min
5. [API_REFERENCE.md](API_REFERENCE.md) - 15 min
6. **Experiment with configurations**

### Path 3: Developer (1 day)

1. [README_PROJETO.md](README_PROJETO.md) - 15 min
2. [ARCHITECTURE.md](ARCHITECTURE.md) - 60 min
3. [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) - 30 min
4. [FILE_ROLES.md](FILE_ROLES.md) - 30 min
5. [INTEGRATION_REFACTOR_SUMMARY.md](INTEGRATION_REFACTOR_SUMMARY.md) - 45 min
6. [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md) - 60 min
7. [integration/map_creation_integration.md](integration/map_creation_integration.md) - 45 min
8. [API_REFERENCE.md](API_REFERENCE.md) - 45 min
9. **Review source code**

### Path 4: Contributor (2-3 days)

Complete Path 3, then:
1. Study integration examples in [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)
2. Review recent changes in [CHANGELOG_AUTOGERADO.md](CHANGELOG_AUTOGERADO.md)
3. Read [RELATORIO_ERROS_ANALISE.md](RELATORIO_ERROS_ANALISE.md) for common issues
4. Review test files in `tests/`
5. Understand integration patterns by reading:
   - [interface/services/nsga_cached_integration.py](../interface/services/nsga_cached_integration.py)
   - [interface/services/map_creation_integration.py](../interface/services/map_creation_integration.py)
6. **Start contributing!**

---

## 🔍 Finding Specific Information

### "How do I configure NSGA-II?"

→ [UNIFIED_CONFIG_FORMAT.md](UNIFIED_CONFIG_FORMAT.md)  
→ [examples/nsga_ii/unified_config.json](../examples/nsga_ii/unified_config.json)

### "What does file X do?"

→ [FILE_ROLES.md](FILE_ROLES.md)

### "How do I use function Y?"

→ [API_REFERENCE.md](API_REFERENCE.md)

### "How was feature Z implemented?"

→ [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)  
→ [CHANGELOG_AUTOGERADO.md](CHANGELOG_AUTOGERADO.md)

### "Why is NSGA-II cached faster?"

→ [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md) - Performance section

### "What are the color codes for maps?"

→ [integration/map_creation_integration.md](integration/map_creation_integration.md) - Color scheme

### "How do I integrate a new module?"

→ [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) - See examples  
→ [INTEGRATION_REFACTOR_SUMMARY.md](INTEGRATION_REFACTOR_SUMMARY.md) - Use integration API

---

## 📊 Documentation Statistics

**Total Documents:** 20+ files  
**Total Lines:** 15,000+ lines  
**Quick References:** 2 documents  
**Complete Guides:** 6 documents  
**Summaries:** 4 documents  
**References:** 4 documents  
**Examples:** 3+ documents  

**Coverage:**
- ✅ System architecture
- ✅ NSGA-II (standard and cached)
- ✅ Map creation
- ✅ Integration layer
- ✅ Interface/UI
- ✅ API reference
- ✅ Configuration formats
- ✅ Examples and tutorials

---

## 🎯 Most Important Documents

If you only read 5 documents, read these:

1. **[INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)** - See everything that's been built
2. **[NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md)** - Get started fast
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand system design
4. **[integration/map_creation_integration.md](integration/map_creation_integration.md)** - Create maps
5. **[API_REFERENCE.md](API_REFERENCE.md)** - Use the APIs

---

## 🆕 Latest Documentation

**Most Recently Updated:**

1. [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) - Oct 23, 2025
2. [NSGA_CACHED_FINAL_SUMMARY.md](NSGA_CACHED_FINAL_SUMMARY.md) - Oct 23, 2025
3. [NSGA_CACHED_INTEGRATION.md](NSGA_CACHED_INTEGRATION.md) - Oct 23, 2025
4. [NSGA_CACHED_QUICK_REFERENCE.md](NSGA_CACHED_QUICK_REFERENCE.md) - Oct 23, 2025
5. [INDEX.md](INDEX.md) - Oct 23, 2025 (this file)

---

## 📞 Need Help?

**Can't find what you need?**

1. Check [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) for overview
2. Search this INDEX.md for keywords
3. Browse the relevant category above
4. Check [FILE_ROLES.md](FILE_ROLES.md) for file locations
5. Review [API_REFERENCE.md](API_REFERENCE.md) for function details

**Still stuck?**

- Check [RELATORIO_ERROS_ANALISE.md](RELATORIO_ERROS_ANALISE.md) for common issues
- Review test files in `tests/` for usage examples
- Look at integration services in `interface/services/` for patterns

---

**Last Updated:** October 23, 2025  
**Documentation Version:** 2.0  
**System Status:** ✅ Production Ready
