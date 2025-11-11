## Relatório Técnico do Sistema Especialista DermaBot (Versão com Árvore de Decisão)

Disciplina: Inteligência Artificial
Período: 2025.2
Professora: Cristina Bicharra
Grupo: Carolina Lutterbach, Felipe Amaro e Thaís Deluca

## 1. Introdução
O DermaBot é um chatbot voltado para o reconhecimento e orientação inicial das principais doenças dermatológicas. O sistema foi desenvolvido em Python e integra três componentes principais:
- Árvore de decisão manual (arvoreDecisao.py): modela o raciocínio clínico de diagnóstico com base em sintomas, sinais e localização.
- Motor de navegação (motorArvore.py) — percorre a árvore conforme as respostas do usuário e determina o próximo nó (pergunta) ou folha (diagnóstico).
- Interface local (appDermaBotArvore.py) — fornece a interação textual no navegador (perguntas, respostas e resultados).
A proposta dessa versão é substituir o motor baseado em MYCIN (CNF e fatores de certeza) por uma estrutura determinística, transparente e explicável, baseada em árvore de decisão.

## 2. Arquitetura do Sistema
### 2.1 Estrutura geral
DermaBot/
appDermaBotArvore.py     # Interface Flask local
motorArvore.py           # Motor de decisão e heurística contextual
arvoreDecisao.py         # Base de conhecimento (árvore manual)
O usuário interage via navegador.
O Flask envia e recebe mensagens assíncronas (JavaScript/JSON).
O motor de decisão processa cada resposta, atualiza o estado e seleciona a próxima pergunta.
Quando atinge uma folha, o sistema exibe o diagnóstico sugerido, a justificativa clínica e as orientações básicas.

### 2.2 Fluxo lógico
Início: O sistema exibe mensagem de boas-vindas e pergunta se o usuário deseja iniciar o diagnóstico.
Percurso da árvore: Cada nó contém uma característica clínica (caracteristica) e uma pergunta (pergunta).
Os ramos representam as respostas possíveis: 1 (Sim) e 2 (Não).
As folhas contêm o diagnóstico e suas orientações.
Conclusão: Ao atingir uma folha, o bot mostra o resultado e oferece a opção de reiniciar.

## 3. Heurística Contextual de Interpretação de Texto
Para permitir que o usuário responda de forma natural (por exemplo, digitando “predominantemente bolhosas” ou “não há vesículas”), foi incorporada ao motorArvore.py uma heurística linguística simples que traduz o texto livre em respostas binárias (sim/não), sem alterar a estrutura da árvore.

### 3.1 Regras da heurística
- Negação explícita → “não” (2):
Se o texto contém palavras como “não”, “sem”, “ausência”, “negativo”, o sistema interpreta como 2.
- Afirmação explícita → “sim” (1):
Palavras como “sim”, “ok”, “positivo”, “certo” mapeiam para 1.
- Contexto sem negação → “sim” (1):
Caso a resposta mencione termos presentes na pergunta (“vesicular”, “bolhosa”, “descamação”, “prurido” etc.), o sistema assume que o usuário está afirmando a característica perguntada.
- Empate ou ambiguidade:
Se o texto não contiver pistas suficientes, o bot repete a pergunta sugerindo respostas 1 ou 2.

### 3.2 Exemplo prático
Pergunta: “As lesões são predominantemente vesiculares ou bolhosas?”
Respostas possíveis e interpretação automática:
Resposta digitada
Interpretação
Valor
“Sim”
Afirmação explícita
1
“Não”
Negação explícita
2
“Predominantemente bolhosas”
Mesmos termos da pergunta
1
“Não há vesículas”
Contém negação
2
“As lesões são secas e descamativas”
Sem menção a “vesículas”
2

## 4. Benefícios da Versão com Árvore de Decisão
Aspecto
Vantagem
Transparência
Cada decisão é explícita e reproduzível; não há cálculos ocultos de fatores de certeza.
Rastreabilidade clínica
Cada folha corresponde a um conjunto coerente de sintomas/signos observáveis.
Explicabilidade
O bot apresenta o raciocínio (“Por quê: ...”) e as orientações associadas.
Facilidade de validação
Especialistas podem revisar as perguntas e ramos sem conhecimento técnico.
Compatibilidade educacional
O fluxo simula o raciocínio clínico humano, sendo ideal para ensino.

## 5. Lista de Doenças Contempladas
A árvore contempla as seguintes doenças dermatológicas, extraídas de estudos e da consulta a um dermatologista especialista.
Micoses superficiais
Sífilis
Hanseníase
Herpes simples
Dermatite atópica
Dermatite de contato (irritativa/alérgica)
Dermatite de estase
Eczema disidrótico
Líquen simples crônico
Dermatite seborreica
Psoríase
Pitiríase rósea
Eritrodermia esfoliativa
Parapsoríase (suspeita)
Eritema multiforme
Eritema nodoso
Impetigo
Escabiose
Candidíase cutânea
Urticária
Rosácea
Vitiligo
Molusco contagioso
Queratose actínica
Carcinoma basocelular

## 6. Limitações e Possíveis Extensões
Tipo
Descrição
Linguagem natural
A heurística cobre respostas curtas; textos longos ou ambíguos ainda podem exigir repetição.
Escalabilidade
A árvore é manual; para expandir, pode-se derivar novas subárvores a partir de dados clínicos.
Interface
A interação textual pode futuramente ser complementada por upload de imagens (análise visual).
Registro de percurso
Pode ser adicionado log completo de decisões para fins didáticos ou de auditoria.

## 7. Conclusão
A implementação atual do DermaBot (versão Árvore de Decisão) mantém a precisão e interpretabilidade do raciocínio clínico, eliminando a necessidade de fatores de certeza do MYCIN.
Com a heurística contextual, o chatbot passa a compreender respostas em linguagem natural, o que melhora a usabilidade e a aceitação em ambientes educacionais e clínicos simulados.
O resultado é um sistema determinístico, explicável e didático, fiel à lógica do Expert SINTA, mas atualizado para o contexto de interação atual.
