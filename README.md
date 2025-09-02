# 3Cat-assistent

# 3Cat-Assistent

En aquest repositori es troben **tres projectes diferenciats**, cadascun amb el seu propi enfocament i objectius dins del marc general de l’**assistent 3Cat**.  
Els projectes són els següents:

- `assistent-basic`  
  Aquest projecte conté un **backend i un frontend molt senzills**, pensats per fer **proves ràpides sobre els nodes generals**.  

  - **Backend**: permet cridar de manera independent les *prompts* dels diferents criteris (pluralisme, diversitat, etc.), sense utilitzar encara LangGraph. Està dissenyat només com a entorn de proves i validació inicial.  
  - **Frontend**: és una pàgina HTML bàsica que fa peticions al servidor backend per mostrar els resultats.  

  En resum, és un entorn lleuger que serveix per experimentar i validar el funcionament dels criteris de manera aïllada abans d’integrar-los en fluxos més complexos.

- `assistent-lang-chain`  
  Té la mateixa estructura que l’`assistent-basic`, amb un **backend** i un **frontend**, però aquí el backend és molt més complet.  

  - **Backend**: inclou tota l’estructura de **LangGraph**, de manera que els diferents nodes i criteris funcionen conjuntament dins d’un mateix flux. Ja no es tracta de provar els criteris per separat, sinó de tenir l’**arquitectura de l’assistent final** en funcionament.  
  - **Frontend**: igual que a la versió bàsica, és una interfície HTML que interactua amb el backend, però ara el servidor retorna els resultats seguint el flux complet definit a LangGraph.  

  Aquest projecte representa la versió més avançada, amb l’assistent treballant de manera integrada.

- `assistent-linguistic`  
  És un projecte en desenvolupament pensat per treballar els **criteris més lingüístics** del llibre d’estil.  

  - A diferència dels altres projectes, aquí **no s’hi tracten els criteris generals** (pluralisme, diversitat, etc.), sinó que s’està dissenyant un **assistent separat** que es centrarà en aspectes lingüístics específics.  
  - De moment, segueix la mateixa estructura que l’`assistent-lang-chain`, amb un **backend** (basat en LangGraph) i un **frontend** senzill en HTML que interactua amb el servidor.  

  L’objectiu és que acabi sent un mòdul complementari a l’assistent general, especialitzat en l’anàlisi lingüística.

---

Cada carpeta conté el codi i els recursos necessaris per al desenvolupament i execució del seu corresponent projecte.  
Aquest README serveix com a punt d’entrada general, mentre que dins de cada projecte es pot afegir un README més detallat amb instruccions específiques d’instal·lació i ús.

## Detalls de cada assistent

En aquest apartat s’entra en **més profunditat** en cadascun dels tres projectes.  
S’hi descriu l’**estructura bàsica** (backend i frontend), les tecnologies utilitzades i l’estat de desenvolupament actual.  
Això permet entendre millor el rol de cada assistent dins del conjunt del sistema.

### 🟢 assistent-basic
- **Estructura**: backend senzill + frontend HTML.  
- **Funcionalitat principal**: proves independents de cada criteri, sense flux integrat.  
- **Ús previst**: validació ràpida dels nodes generals abans d’integrar-los a LangGraph.  

### 🟡 assistent-lang-chain
- **Estructura**: backend complet amb LangGraph + frontend HTML.  
- **Funcionalitat principal**: flux global de l’assistent amb tots els criteris integrats. Nodes específics inclosos, encara sense funcionalitat.
- **Ús previst**: és la base de l’arquitectura final de l’assistent.  

### 🟠 assistent-linguistic
- **Estructura**: backend simple + frontend HTML (similar a l’assistent-basic).  
- **Funcionalitat principal**: treball específic amb criteris lingüístics del llibre d’estil, independent dels criteris generals.  
- **Ús previst**: complementar l’assistent general amb un mòdul dedicat a l’anàlisi lingüística.
