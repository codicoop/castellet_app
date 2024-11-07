# Castellet Sostenible

## 1. Resum de l'aplicació

### 1.1 Client i descripció del projecte

[Castellet Sostenible SCCL](https://castelletsostenible.cat/) és una cooperativa energètica de [Sant Vicenç de Castellet](https://maps.app.goo.gl/zVqeNzcFZXHEzVQm9), que neix amb l'objectiu d'impulsar la transició energètica i aconseguir un model energètic 100% renovable, de proximitat i a mans de la ciutadania, anteposant de forma clara i transparent els propòsits de millora social i mediambiental als guanys econòmics.

### 1.2 Objectiu, l'aplicació s'ha de resoldre

La finalitat de l'aplicació és la de crear un espai per les sócies de la cooperativa, per vitsualitzar documents dels diferents projectes que formen part.

### 1.3 Tipus de roles

Els usuaris de l'aplicació tenen la particularitat que el campo `email` és opcional. Per això, el login es podrà fer també amb el DNI i tota la part de verificació de correu electrònic no caldrà.

- <u>Usuari administrador</u>: Encarregat de registrar usuaris, crear projectes i pujar documents associats a projectes. També podrán descarregar documents en format _.csv_ amb la informació dels projectes, dels usuaris o de la newsletter.
- <u>Usuari normal</u>: La resta d'usuaris només tendran accés a l'aplicació per visualitzar i descarregar els documents. No podran fer el registre, ni editar el seu perfil (només la contrasenya), ni pujar documents.

  L'usuari pot pertànyer a diversos projectes pel que podrà visualitzar els documents associats a aquests projectes.
  Dins d'aquest tipus de usuari, és fa la distinció de si pertany al consell rector o no i només afectarà a la visualització de certs documents marcats des de el panell admin.

## 2. Configuració del projecte

1. Descarregar el repositori en el teu ordinador amb `git clone https://github.com/codicoop/castellet_app.git`
2. Assegura't que tens instal·lada la versió correcta de Python, comprovant en l'arxiu _docker/Dockerfile_ y el _pyproject.toml_ i haurà de ser la mateixa versió. Després, executa `python -V` en l'arrel, per saber la versió de Python que està fent servir el teu ordinador.
3. Si la versió és diferent, fes servir [Pyenv](https://github.com/pyenv/pyenv) per instal·lar la versió correcta amb el comandament `pyenv local x.xx.xx`
4. Executa `poetry install` i `npm install` en l'arrel, per instal·lar els packages necessaris.
5. Si vas a fer canvis en els estils HTML, has de compilar-los perquè es mostrin. Ho fas amb: `npx tailwindcss -i ./src/assets/styles/input.css -o ./src/assets/styles/output.css --watch`
6. Canviar de nom el fitxer docker/.env.example a docker/.env, i acabar d'ajustar variables si és necessari. Per la pujada d'arxius, omplir la part de `Media / Storage` ambs les dades de Wasabi.
7. Anar a la consola Docker i executar: `python manage.py migrate`.
8. Entrar a la versió en local a través de: [localhost:1501](http://localhost:1501)

## 3. Stack usat

- Docker
- Pyenv
- Poetry
- JavaScript
- Tailwind
- htmx
- Flowbite
- Python 3.11
- Django
- Django Wagtail
