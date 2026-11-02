# Modelo de registro de decisão técnica (ADR)

Crie um arquivo `decisoes/ADR-NNNN-assunto.md` quando for necessário decidir entre alternativas técnicas. **Não substituir esta documentação por commits executáveis sem autorização.**

```markdown
# ADR-NNNN — Título

- Data: AAAA-MM-DD
- Status: Proposta | Em estudo | Aceita | Rejeitada | Substituída
- Autor da análise:
- Decisor / homologador: proprietário Makernauta
- Baseline SHA:
- Experimento / PR relacionada:

## Problema
Qual problema observável precisa ser resolvido?

## Contexto e fontes
Link para documentos oficiais e projetos estudados, data de consulta e versões analisadas. Indicar licença e direitos quando aplicáveis.

## Fatos demonstrados
O que é certo por fonte técnica ou teste. Evidências e limites.

## Hipóteses
O que *ainda não foi comprovado*.

## Alternativas
| Alternativa | Vantagem | Limite / custo | Licença / segurança |
|---|---|---|---|

## Decisão proposta
Qual alternativa e por quê? Se não foi aprovada, manter como *proposta*.

## Plano de verificação
Entradas, resultado esperado, comparação, regressões, desempenho, validação visual e pós-processador.

## Restrições
Arquivos protegidos, modo 3+1 e G-code, segurança CNC, direitos de terceiros.

## Consequências, reversão e pendências
Quem decide, como reverter, o que medir antes de avançar.

## Aprovação
Data, autor da homologação, SHA e link da PR. Se ausentes: **não homologado**.
```

**Regra:** a decisão não pode extrapolar a evidência; documento não é liberação para operar CNC real. Ao substituir uma ADR, manter histórico e linkar sua sucessora.
