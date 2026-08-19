# Cartório de citações dos 207 expoentes (projeto IAP)

Este arquivo é a especificação permanente da tarefa. Toda sessão do Claude Code aberta nesta pasta
o carrega automaticamente. Não é preciso repetir as regras no comando: o comando de lote traz só os
parâmetros.

## Estrutura da pasta

```
citacoes-207/
├── CLAUDE.md                        (este arquivo)
├── _registro-citacoes.jsonl         (índice de retomada: quem já foi feito)
├── dados/
│   ├── CATALOGO_207_EXPOENTES_v05.xlsx        (os 207, aba Catálogo_207)
│   └── OURO_V02_96nomes_52ferramentas.xlsx    (as 96 frases sem fonte, aba Fusão Completa)
├── saida/
│   └── CITACOES_207_vNN.xlsx        (a planilha mestre; NN cresce a cada lote)
└── scripts/
    └── trava.py                     (checagem mecânica anti-invenção)
```

## Comando de lote (é isto que se digita a cada sessão)

```
Rode o lote 1: 8 autores, profundidade A.
```

Parâmetros aceitos e seus padrões:

```
lote .............. número sequencial, só para o relatório
autores ........... quantos processar nesta sessão (padrão 8)
profundidade ...... A = 3 citações para os 93 · B = 3 só para os 12 principais, 2 para os outros 81
```

## Como manipular a planilha

**Sempre por script, nunca por leitura.** Use `openpyxl` em Python para abrir, acrescentar linha e
salvar. O conteúdo da planilha não deve entrar na janela de contexto: é ela que carrega 621 linhas,
e lê-la a cada autor é o desperdício que este desenho existe para evitar.

Para saber onde parou, leia `_registro-citacoes.jsonl`, que é curto de propósito. Nunca varra a
planilha para descobrir o que já foi feito.

Busca na internet está autorizada nesta tarefa, sem pedir confirmação, com o piso de confiabilidade
de 95% e o registro obrigatório da URL de onde a prova foi recuperada.

---

## 1. A LEI QUE ESTÁ ACIMA DE TODAS AS OUTRAS

**Nunca inventar. Nunca.** Não existe circunstância (pressa, lote grande, frase quase certa,
usuário insistindo) em que preencher uma lacuna com material plausível seja aceitável.

Está proibido, sem exceção:

- locus, página, fólio, versículo, linha, parágrafo, número de carta
- o texto no idioma original: ele é **recuperado**, nunca reconstruído de memória
- como uma edição publicada verte a frase (isso põe palavras na boca de um tradutor identificável)
- nome de tradutor, editora, cidade, ano
- data de primeira aparição
- precisão maior que a da fonte ("Livro V" não vira "V.12")
- a terceira citação, quando só duas passaram

**Entregar vazio é resultado válido e honesto.** "Não localizei" tem valor. Uma nota bonita e falsa
não tem nenhum: ela contamina a credibilidade de todo o livro, não só daquele rodapé.

**Trava mecânica de verificação.** Nenhuma linha pode receber selo `PRIMÁRIA` ou `CONTEMPORÂNEA`
com a coluna `Fonte recuperada (URL)` vazia. Se você não tem o endereço de onde recuperou a prova,
o selo cai para `ATRIBUÍDA`. Ao fim de cada lote, rode essa checagem e reporte o resultado.

**Proibido copiar texto corrido de fontes pesquisadas.** A citação em si é o objeto do trabalho e
entra literal; qualquer explicação ao redor dela é escrita com suas próprias palavras.

---

## 2. O QUE ESTA TAREFA PRODUZ

Para cada expoente, um **par de transplante**: duas linhas que o autor cola direto no manuscrito.

```
CORPO   → "O que eu não sei, tampouco julgo saber."¹
RODAPÉ  → ¹ Sócrates, em PLATÃO. Apologia de Sócrates, 21d. Texto grego: Perseus Digital
            Library. Tradução do grego para o português por IA.
```

A citação é o subproduto. **A prova é o produto.** A pergunta que você responde não é "o que fulano
disse de bonito", é "onde está escrito, e como sei que está".

---

## 3. O UNIVERSO E AS TRILHAS

207 expoentes no `CATALOGO_207_EXPOENTES_v05.xlsx`, aba `Catálogo_207`.

| Trilha | Quem | Quantos | Meta | Modo de entrada |
|---|---|---|---|---|
| A | Os 12 gênios principais (coluna `Principal` preenchida) | 12 | 3 citações | AUDITORIA + BUSCA |
| B | Citados com frase já registrada no projeto | 81 | 3 (ou 2, se PROFUNDIDADE = B) | AUDITORIA + BUSCA |
| C | Só constam do anexo | 111 | 1 citação | BUSCA |

**Atenção ao mapeamento de nomes.** O `OURO_V02` traz 96 linhas com a coluna `💬 Citação Famosa`
preenchida, mas correspondem a **93 pessoas distintas**: Churchill, Stalin e Gandhi aparecem
duplicados com grafias diferentes. Use sempre o **nome canônico do catálogo dos 207**, e resolva as
variantes abreviadas (Churchill → Winston Churchill; Laozi → Lao Tsé; Bismarck → Otto von Bismarck;
Marcus Aurelius → Marco Aurélio; Hipátia → Hipátia de Alexandria; Heron Alexandria → Heron de
Alexandria; e assim por diante).

**Ordem de execução:** trilha A completa, depois B, depois C. Dentro de cada trilha, ordem numérica
do catálogo.

---

## 4. O CICLO: UM AUTOR POR VEZ

Repita este ciclo até esgotar os autores do lote. **Grave a planilha ao fim de cada autor**, não
ao fim do lote. Uma interrupção pode custar um autor, nunca oito.

1. **Consultar o registro.** Se o autor já consta em `_registro-citacoes.jsonl` com status
   `FECHADO`, pule e anote que pulou. Não refaça trabalho.
2. **Situar o autor antes de buscar.** Em que idioma escreveu, século, corpus existente, sistema de
   referência canônico, arquivo dedicado (se houver) e teto de selo. Isso muda a busca inteira:
   procurar Kant por página de tradução brasileira acha nada, procurar por Akademie-Ausgabe acha
   tudo.
3. **Auditar a frase que já está no projeto** (trilhas A e B). Veredito obrigatório: CONFIRMA,
   CORRIGE, REBAIXA ou CONDENA. Ver §6.
4. **Levantar 5 a 8 candidatos** ao pódio, mais do que o necessário.
5. **Verificar candidato por candidato.** Ver §5.
6. **Selar e escrever as linhas** na planilha. Ver §7 e §8.
7. **Gravar o arquivo e acrescentar a linha no `.jsonl`.** Só então passe ao próximo autor.

---

## 5. PROTOCOLO DE VERIFICAÇÃO

### Escada de prova (o nível da melhor prova determina o selo)

| Nível | O que é | Sustenta |
|---|---|---|
| N1 | Texto da própria obra em repositório crítico ou digitalização, com locus visível | `PRIMÁRIA` |
| N2 | Edição crítica ou arquivo dedicado ao autor (Loeb, Akademie-Ausgabe, Collected Works, Founders Online, Newton Project) | `PRIMÁRIA` |
| N3 | Registro contemporâneo de terceiro presente: transcrição de discurso, entrevista datada em veículo identificado, jornal da época, ata, carta de quem ouviu | `CONTEMPORÂNEA` |
| N4 | Biografia ou estudo acadêmico que cita a frase, sem locus primário rastreável | `ATRIBUÍDA` |
| N5 | Antologia geral de citações sem referência interna | `ATRIBUÍDA` fraca |
| N6 | Agregador, rede social, card, listicle | prova de nada, só de circulação |

**N6 nunca sobe ninguém.** Se toda a evidência de uma frase é N6, o selo é `APÓCRIFA` presumida, e
a observação registra "nenhum registro acima de agregador".

### Regra dos dois olhos

Um locus vira `PRIMÁRIA` quando **(a)** uma fonte N1 ou N2 o exibe, **ou** **(b)** duas fontes
independentes de nível ≤N3 apontam o **mesmo** locus. "Independentes" exclui duas páginas do mesmo
site, dois artigos que citam a mesma terceira fonte, duas traduções do mesmo verbete.

Coincidência de **texto** sem coincidência de **locus** não conta. É assim que o erro se propaga:
todo mundo copia a frase, ninguém copia o endereço.

### Os quatro testes (aplicar a todo candidato, inclusive aos "obviamente" verdadeiros)

1. **Idioma original.** O autor escreveu em grego, latim, alemão, russo? A frase tem de existir
   naquela língua. Se só existe em inglês e português, o teto é `ATRIBUÍDA`, com suspeita de
   fabricação anglófona.
2. **Primeira aparição.** Date a ocorrência mais antiga que conseguir. Aparição em vida e ligada à
   obra é bom sinal. Décadas ou séculos após a morte, sem elo com o corpus, é suspeita forte.
   Aparição mais antiga já trazendo "atribuído a" é sinal clássico de lenda.
3. **Intermediário.** Muita citação é paráfrase de biógrafo que virou aspas por repetição. Nomeie o
   intermediário e recue o selo. Quem estava na sala é N3; quem escreveu 200 anos depois é N4,
   mesmo sendo historiador respeitável.
4. **Migração.** A mesma frase atribuída a duas ou três pessoas diferentes quase sempre significa
   que não é de nenhuma delas: é provérbio que foi ganhando padrinhos famosos.

### Regra de parada

**Máximo 4 ângulos de busca distintos por citação.** Ângulos distintos significa formulações
materialmente diferentes; trocar uma palavra não conta. Esgotados, sele no que a prova sustenta,
escreva a lacuna e siga. Insistência não fabrica evidência.

Ângulos que rendem, nesta ordem: trecho literal + nome da obra provável · trecho no idioma original
· trecho + termo do sistema de referência (`Stephanus`, `Bekker`, `Akademie`, `CPAE`, `fol.`) ·
trecho + "misattributed" / "apócrifa" / "never said" · nome do autor + repositório dedicado ·
trecho + "earliest" ou data anterior à morte.

**Nunca comece por "melhores frases de X".** Essa busca devolve o esgoto dos agregadores. Para achar
as mais famosas de alguém: antologia de referência + literatura crítica sobre o autor + as passagens
que a própria erudição trata como célebres.

### Repositórios que costumam resolver

Perseus Digital Library · Loeb Classical Library · Corpus Thomisticum · Internet Archive ·
HathiTrust · Gallica · Project Gutenberg · Founders Online · Darwin Correspondence Project ·
Einstein Papers Project · Newton Project · Mark Twain Project · Hansard · Quote Investigator (a
melhor metodologia de datação de primeira aparição que existe) · seções "Misattributed" do Wikiquote
(pista boa, nunca prova).

---

## 6. OS CINCO SELOS E OS QUATRO VEREDITOS

| Selo | Significa | Sobe ao pódio? |
|---|---|---|
| `PRIMÁRIA` | Locus exato na obra do próprio autor | Sim |
| `CONTEMPORÂNEA` | O autor disse, e registro documental de quem estava presente preserva. O intermediário é nomeado | Sim |
| `ATRIBUÍDA` | Circula em fonte crível, nenhum locus primário localizado | Não |
| `DISPUTADA` | A erudição contesta a autoria ou a formulação | Não |
| `APÓCRIFA` | Demonstradamente não é dele. Nomear a origem real | Não |

**Teto estrutural.** Alguns nunca alcançam `PRIMÁRIA` por razão estrutural: não escreveram nada.
Sócrates (via Platão e Xenofonte), Jesus (evangelistas), Buda (cânone páli tardio), Confúcio
(*Analectos*, compilado por discípulos), Pitágoras (nada sobreviveu), Diógenes e os cínicos
(Diógenes Laércio, séculos depois), Alexandre, Hamurabi na parte lendária. Declare o teto na
observação em vez de fingir acesso direto.

**Vereditos da auditoria**, em ordem de preferência:

1. **CONFIRMA**: a frase é dele e o locus foi achado.
2. **CORRIGE**: a ideia é dele, a formulação circulante não. Entregue a formulação real com locus
   e mostre o que mudou.
3. **REBAIXA**: não achou locus. Selo `ATRIBUÍDA`. O autor pode manter, desde que escreva
   "atribuído a" em vez de "escreveu". Diga isso explicitamente na observação.
4. **CONDENA**: apócrifa. **Sempre acompanhe de substituta**: uma citação verificada do mesmo autor
   que cumpra a mesma função retórica. Derrubar sem repor deixa buraco, e buraco tende a ser
   preenchido de novo pela apócrifa.

**A apócrifa famosa é achado de primeira ordem, não lixo.** Descobrir que a frase mais célebre de um
gênio nunca foi dita por ele vale mais que a citação verdadeira: é matéria-prima do livro, e evita um
erro impresso.

---

## 7. A PLANILHA: ESTRUTURA EXATA

Abra a versão mais recente de `saida/CITACOES_207_vNN.xlsx`, **acrescente linhas** e salve com o
número de versão seguinte (`v03`, `v04`…). Nunca recrie o arquivo do zero. Nunca altere linhas de
autores já fechados. A versão anterior fica em disco: é o histórico, e serve de rollback se um lote
sair torto.

### Aba `CITACOES` (uma linha por citação)

`Nº` · `Nome canônico` · `Ordem` · `CORPO (colar no livro)` · `RODAPÉ (nota pronta)` ·
`Texto original` · `Idioma` · `Obra` · `Locus` · `Edição / texto-base` · `Selo` · `Pódio?` ·
`Nível` · `Fonte recuperada (URL)` · `Conf. %` · `Domínio público?` · `Data` · `Observação`

Autor que fecha com menos citações que a meta recebe as linhas restantes com `(vaga aberta)` no
CORPO e, na observação, **o candidato nomeado e o motivo de não ter entrado**. Isso é deliberado:
completar pódio com material fraco é o erro que este trabalho existe para impedir.

### Aba `AUDITORIA_96`

`Nº` · `Nome canônico` · `Frase hoje no projeto` · `Veredito` · `Selo` · `O que a prova mostra` ·
`Substituta` · `Prioridade` · `Data`

O campo `O que a prova mostra` é onde mora o valor. Escreva o que procurou, o que achou e o que não
achou, em prosa sua, com datas e nomes.

### Aba `APOCRIFAS`

`Nº` · `Autor` · `Frase que circula` · `Origem real` · `Primeira aparição` · `Padrões de fabricação`
· `Nota de defesa`

A nota de defesa tem três movimentos e no máximo três linhas: **o que não existe** → **onde está o
real** → **de onde veio a lenda**. Serve para o caso de o autor querer manter a frase falsa como
assunto do texto em vez de removê-la.

### Aba `PLACAR`

Atualize `Fechadas` e `Status` de cada autor tocado. Status possíveis: `não iniciado`,
`EM ANDAMENTO`, `FECHADO`.

### `Domínio público?`

`Sim` se o autor morreu há mais de 70 anos. `NÃO (morreu em AAAA)` caso contrário. É coluna de
triagem para o autor decidir, não parecer jurídico. Nos casos `NÃO`, mantenha a citação curta.

---

## 8. O RODAPÉ: NORMA A, FIXA NAS 207

```
{Personagem, em }AUTOR. Obra, locus. {Texto {idioma}: {edição crítica}. }Tradução do {origem} para o português por IA.
```

- **O locus canônico nunca sai.** Página de tradução muda a cada edição; Stephanus, Bekker e
  Akademie não mudam nunca. É o locus que faz a nota sobreviver.
- **A origem da tradução nunca sai.** Em toda citação traduzida, a nota diz
  `Tradução do {idioma} para o português por IA.` Não existe forma curta, não existe "idem", não
  existe abreviação a partir da segunda ocorrência. Cada nota tem de sobreviver a ser lida sozinha.
- **Autor sem obra própria leva duas camadas**: a frase é de Sócrates, a fonte é Platão. Escreva
  `Sócrates, em PLATÃO. Apologia de Sócrates, 21d.` Atribuir a obra ao personagem é erro de
  atribuição.
- **Edição publicada só quando o texto estiver em mãos.** Saber que a edição existe e quem a
  traduziu **não autoriza** supor como ela verte a frase: isso seria invenção com vítima nomeada.
  Sem o texto, use a tradução por IA e não mencione a edição.
- **Corpo sem enfeite**: só a frase, entre aspas, com a marca da nota. Nada de colchetes, reticências
  ou glosa. Se a citação precisa de contexto para não enganar, o contexto vai no **rodapé**.
- **Aspas só em formulação literal.** Se o que você tem é paráfrase, o corpo pede "como disse X" sem
  aspas.

Formatos por tipo de fonte:

```
Obra clássica     AUTOR. Obra, locus canônico.
Livro moderno     SOBRENOME, Inicial. Título, § ou cap. Trad. X. Cidade: Editora, ano.
Carta             AUTOR. Carta a {destinatário}, {data}. {Arquivo}, {referência}.
Discurso          AUTOR. Discurso em {local}, {data}. {Fonte da transcrição}.
Entrevista        AUTOR. Entrevista a {entrevistador}. {Veículo}, {data}.
Caderno / códice  AUTOR. {Códice}, fól. {n}. {Coleção}.
```

---

## 9. ARMADILHAS JÁ IDENTIFICADAS NO PILOTO

Estas quatro apareceram nos primeiros quatro autores. Procure-as ativamente em todos os demais.

**1 · O autor está citando outra pessoa.**
Lincoln pôs "uma casa dividida contra si mesma não pode permanecer de pé" **entre aspas** no próprio
manuscrito, porque estava citando o Evangelho (Marcos 3:25). A citação é primária como discurso, mas
atribuir a autoria da **sentença** a ele é erro. Sempre verifique se há aspas, itálico ou marca de
citação no texto original.

**2 · A oração amputada que inverte o sentido.**
Churchill disse "nunca ceda, exceto às convicções de honra e bom senso". A versão popular apaga a
exceção e transforma persistência com juízo em teimosia incondicional. Quando a frase circulante for
mais curta que a original, verifique **o que foi cortado** antes de aceitar o corte.

**3 · O "original" que é tradução de tradução.**
"Só sei que nada sei" nasceu em latim (Cícero, Nicolau de Cusa) e foi retrovertida para o grego
moderno. Quem cita o grego está citando uma tradução do latim feita séculos depois. Se o suposto
original só aparece em grafia moderna, desconfie.

**4 · Duas fontes reputadas com números divergentes.**
Para a mesma passagem de *Il Saggiatore*, o Museo Galileo dá `Ed. Naz. VI, 255` e o DISF dá
`vol. VI, p. 232`. Quando fontes boas divergem, **o número não entra**. Entra o que ninguém contesta
(no caso, o capítulo), e a divergência vai para a observação.

**Ímãs de apócrifa.** Tesla, Leonardo da Vinci, Edison, Sun Tzu, Marco Aurélio, Einstein, Buda,
Gandhi e Steve Jobs atraem frases órfãs pela fama do nome. Ao trabalhar um deles, presuma suspeita e
exija N1/N2 com rigor extra.

**Oito padrões de fabricação:** registro anacrônico (vocabulário de autoajuda na boca de um antigo)
· simetria boa demais (frases reais têm cláusulas sobrando) · nunca vem com endereço · ausência no
idioma original · primeira aparição póstuma e tardia · migração de autor · "atribuído a" já na origem
· utilidade suspeita (serve perfeitamente demais a uma tese moderna).

---

## 10. RELATÓRIO E CHECKPOINT

**A cada autor:** uma linha de status.
```
{Nº}. {Autor} · trilha {A|B|C} · teto {SELO} · {n}/{meta} fechadas · veredito da frase antiga: {X}
```

**A cada 5 autores:** um placar.
```
Placar {a}-{b}: {n} fechados · {n} apócrifas encontradas · {n} com teto estrutural · {n} pendentes
```

**Ao fim do lote:**
1. Salve a planilha na versão seguinte e o `.jsonl` atualizado.
2. Rode a trava mecânica e **cole a saída no relatório**:
   ```bash
   python scripts/trava.py saida/CITACOES_207_vNN.xlsx
   ```
   Se o script apontar FALHA, corrija antes de encerrar o lote. Saída limpa é condição de entrega.
3. Sincronize com o Google Sheets, se e somente se houver conector configurado. Ver §11.
4. Entregue a **lista de decisão do autor**: só os casos `APÓCRIFA` e `ATRIBUÍDA` que estão
   impressos no manuscrito. É o que vira trabalho de revisão.
5. Diga quantos dos 207 faltam e qual é o próximo autor da fila.

---

## 11. SINCRONIZAÇÃO COM O GOOGLE SHEETS

**Etapa opcional.** Se não houver conector de Google Sheets configurado nesta instalação, pule esta
seção inteira, diga que pulou e siga. O trabalho verificado vive no `.xlsx` e no `.jsonl`; o Sheets
é painel, não fonte da verdade.

Havendo conector, executar **uma vez ao fim do lote**, nunca a cada autor. A razão é de custo: cada
leitura ou escrita no Sheets devolve conteúdo para dentro do contexto, enquanto o arquivo local é
manipulado por código sem que o conteúdo seja lido. Sincronizar por autor multiplicaria esse custo
por oito sem nenhum ganho.

### A divisão de papéis, que não se inverte

| Peça | Papel | Quem escreve |
|---|---|---|
| `.xlsx` local | **Fonte da verdade durante a corrida.** É onde o agente lê e escreve, autor por autor | agente, via código |
| `.jsonl` | **Índice de retomada.** Responde "quem já foi feito" sem abrir planilha nenhuma | agente |
| Google Sheets | **Painel vivo.** Espelho para o autor acompanhar e aprovar | agente (espelho) + autor (coluna de aprovação) |

**O estado nunca é lido do Sheets.** Para saber onde parou, consulte o `.jsonl`. Ler o Sheets para
descobrir o que já foi feito é exatamente o desperdício que este desenho existe para evitar.

### Procedimento

1. **Se ainda não existir painel:** crie uma planilha nova chamada `CITACOES_207_PAINEL`, com as
   mesmas cinco abas do arquivo local (`CITACOES`, `AUDITORIA_96`, `APOCRIFAS`, `PLACAR`,
   `LEGENDA`), congele a primeira linha de cada uma e devolva a URL no relatório final, para você guardar. Acrescente
   em `CITACOES` e em `AUDITORIA_96` uma coluna final chamada `APROVAÇÃO DO AUTOR`, deixada vazia.
2. **Se o painel já existir:** acrescente **apenas as linhas criadas neste lote** e atualize as células
   de `Fechadas` e `Status` na aba `PLACAR` dos autores tocados. Não reescreva o arquivo inteiro, não
   reordene, não reformate.
3. **A coluna `APROVAÇÃO DO AUTOR` é intocável.** Ela pertence ao autor. Nunca escreva nela, nunca
   a limpe, nunca a sobrescreva, mesmo que esteja vazia, mesmo em linhas que você mesmo criou.
4. **Divergência entre o Sheets e o arquivo local:** durante a corrida, o arquivo local vence, porque
   é ele que o agente escreve linha a linha. A única exceção é a coluna de aprovação, que só existe
   no Sheets e nunca é comparada.

### Se a sincronização falhar

**Nunca trave o lote por causa disso.** O trabalho verificado já está salvo no `.xlsx` e no `.jsonl`,
que são o que importa. Se o conector não responder, se faltar permissão ou se a URL estiver
inacessível:

1. registre a falha, com o erro exato;
2. siga normalmente e entregue os arquivos locais;
3. avise no relatório final que o painel ficou **um lote atrasado**, e informe qual lote precisa ser
   empurrado na próxima rodada.

Um painel desatualizado é um inconveniente. Um lote perdido é trabalho de verificação jogado fora.

---

## 12. O QUE NÃO FAZER

- Não julgar a beleza nem a utilidade da citação. Julgue a procedência.
- Não escrever o texto do livro ao redor da citação. Não é esta tarefa.
- Não consertar tradução literária. Entregue o original e uma versão fiel, e diga qual é qual.
- Não fechar veredito de autoria contra a erudição estabelecida. Se especialistas divergem, o selo é
  `DISPUTADA` e a observação mostra os dois lados.
- Não usar travessão longo no texto que vai para a planilha. Use parênteses, vírgulas ou dois pontos.
- Não perguntar autorização para buscar na internet: nesta tarefa a busca está autorizada, com o
  piso de confiabilidade de 95% e o registro obrigatório da URL.
- Não parar para perguntar entre um autor e outro. Rode o lote inteiro e pergunte no fim.
- Não ler o Google Sheets para descobrir onde parou. Essa resposta está no `.jsonl`.
- Não sincronizar a cada autor. Uma vez por lote.
- Não escrever na coluna `APROVAÇÃO DO AUTOR`, em hipótese nenhuma.

---

## 13. COMEÇAR

1. Leia `_registro-citacoes.jsonl` e o catálogo dos 207.
2. Confirme em **uma linha**: quantos autores constam como `FECHADO`, quantos faltam, e quais são os
   desta fila.
3. Comece pelo primeiro e não pare até terminar o lote. Não peça autorização entre autores.

Se o `.jsonl` não existir, é a primeira execução: crie-o vazio e comece pela trilha A.
