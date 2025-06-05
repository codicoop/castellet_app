# Castellet Sostenible

## 1. Resum de l'aplicació

### 1.1 Client i descripció del projecte

[Castellet Sostenible SCCL](https://castelletsostenible.cat/) és una cooperativa energètica de [Sant Vicenç de Castellet](https://maps.app.goo.gl/zVqeNzcFZXHEzVQm9), que neix amb l'objectiu d'impulsar la transició energètica i aconseguir un model energètic 100% renovable, de proximitat i a mans de la ciutadania, anteposant de forma clara i transparent els propòsits de millora social i mediambiental als guanys econòmics.

### 1.2 Objectiu, l'aplicació s'ha de resoldre

La finalitat de l'aplicació és la de crear un espai per les sòcies de la cooperativa, per vitsualitzar documents dels diferents projectes que formen part.

### 1.3 Tipus de rols

Els usuaris de l'aplicació tenen la particularitat que el campo `email` és opcional. Per això, el login es podrà fer també amb el DNI i tota la part de verificació de correu electrònic no caldrà.

- <u>Usuari administrador</u>: Encarregat de registrar usuaris, crear projectes i pujar documents associats a projectes. També podrán descarregar documents en format _.csv_ amb la informació dels projectes, dels usuaris o de la newsletter.
- <u>Usuari normal</u>: La resta d'usuaris només tendran accés a l'aplicació per visualitzar i descarregar els documents. No podran fer el registre, ni editar el seu perfil (només la contrasenya), ni pujar documents.

  L'usuari pot pertànyer a diversos projectes pel que podrà visualitzar els documents associats a aquests projectes.
  Dins d'aquest tipus de usuari, és fa la distinció de si pertany al consell rector o no i només afectarà a la visualització de certs documents marcats des de el panell admin.

## 2. Configuració de l'entorn de desenvolupament

Els serveis que necessitaràs son:

- Docker instal·lat (amb docker-compose en cas que l'hagis d'instal·lar a part)
- Postgres: el docker-compose aixecarà tot lo necessari així que no has de proveïr res.
- Enviament de correus: per desenvolupar no et fa falta ja que pots veure els correus a la consola (amb el setting `POST_OFFICE_DEFAULT_BACKEND=django.core.mail.backends.console.EmailBackend`), però en cas que vulguis fer enviaments reals de correu, cal que provisionis o bé un compte de Sendgrid o bé un compte SMTP.
- Pujada de fitxers: l'aplicació està pensada per treballar amb un servei de "object storage" compatible amb S3. Pots provisionar-ne un de real amb el proveïdor que vulguis, o bé aixecar en local un servei que ho emuli.

1. Descarregar el repositori en el teu ordinador amb `git clone https://github.com/codicoop/castellet_app.git`
2. Assegura't que tens instal·lada la versió correcta de Python, comprovant en l'arxiu _docker/Dockerfile_ y el _pyproject.toml_ i haurà de ser la mateixa versió. Després, executa `python -V` en l'arrel, per saber la versió de Python que està fent servir el teu ordinador.
3. Si la versió és diferent, fes servir [Pyenv](https://github.com/pyenv/pyenv) per instal·lar la versió correcta amb el comandament `pyenv local x.xx.xx`
4. Executa `poetry install` i `npm install` en l'arrel, per instal·lar els packages necessaris.
5. Canviar de nom el fitxer docker/.env.example a docker/.env, i acabar d'ajustar variables si és necessari.
6. Per poder pujar fitxers, omplir la part de `Media / Storage` amb les dades del bucket compatible amb S3 que hagis provisionat.
7. Per l'enviament de correus reals, hauràs de modificar la variable `POST_OFFICE_DEFAULT_BACKEND` i omplir la configuració que toqui (SMTP o Sendgrid, segons el que hagis provisionat).
8. Aixecar el contenidor: cal anar a la carpeta `/docker` i executar `docker compose up`.
9. Anar a la consola Docker (ja sigui des de l'entorn visual de Docker o amb `docker exec -it castellet-app bash`) i executar: `python manage.py migrate`.
10. Entrar a la versió en local a través de: [localhost:1501](http://localhost:1501)

## 3. Llibreries, dependències i llenguatges utilitzats

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
- [codi-cooperatiu-internal-tools](https://github.com/codicoop/codi-cooperatiu-internal-tools/)

Les dependències de back-end es gestionen amb Poetry.
Les podeu consultar al `pyproject.toml`.

La llibreria codi-cooperatiu-internal-tools ja no tindrà manteniment. Recomanem
que per poder fer canvis al projecte en un futur, en copieu el codi font cap al
projecte (és a dir, a la carpeta apps/ com a mòdul de Django), i l'elimineu com
a dependència (és a dir, amb `poetry remove codi-cooperatiu-internal-tools`).
Òbviament també caldrà actualitzar el setting `INSTALLED_APPS`.

També la teniu [a PyPi](https://pypi.org/project/codi-cooperatiu-internal-tools/).

El projecte s'ha creat a partir d'aquest boilerplate:
https://github.com/codicoop/boilerplate_django

Mirant-ne el codi i la documentació tindreu informació sobre l'estructura.

## 4. Modificacions al projecte

### 4.1 Canvis als estils (CSS)

El projecte fa servir el framework Tailwind, per tant no hi ha fitxers .css creats
a ma i en principi no hauria falta que creis ni modifiquis cap .css.

Si afegeixes, modifiques o elimines qualsevol classe "css" (que no és CSS sinó
Tailwind en aquest cas) a qualsevol element HTML, has de compilar-los perquè es
mostrin.

Ho fas amb:

    npx tailwindcss -i ./src/assets/styles/input.css -o ./src/assets/styles/output.css --watch

### 4.2 Canvis als textos (traduccions)

Hi ha 3 tipus de textos al projecte:

A. El que forma part del codi en Python (fitxers .py)
B. El que forma part del codi dels templates de Django (fitxers .html)
C. El que es desa a la base de dades (contingut)

En el cas A:
Els textos actuals els trobareu encapsulats en la funció `_("text")`.

En el cas B:
Els trobareu dins del tag `{% translate "text" %}`.

En cas que vulgueu afegir o modificar un text dels casos A i B, els passos a
seguir son:

1. Cal que feu servir aquestes funcions (podeu trobar exemples al codi font).
2. El text original al codi font l'escriviu en anglès.
3. Aixecar l'aplicació (és a dir inicialitzar el contenidor de Docker)
4. Accedir al terminal del contenidor i executar:

    python manage.py makemessages --all

Això farà canvis a una serie de fitxers (depenent de quins canvis hagis fet) amb
extensió .po.

5. Editar un per un els fitxers modificats, recomanem fer servir l'editor [Poedit](https://poedit.net/).
6. Compilar els fitxers traduïts: per defecte el Poedit ho farà automàticament, en qualsevol cas, el comandament (dins la consola del contenidor) és:

    python manage.py compilemessages

7. Reiniciar el contenidor de Docker i els canvis ja haurien d'aparèixer.

**Nota**: En altres projectes de Django, el comandament `makemessages` és
habitual que es pugui executar sense haver d'aixecar l'aplicació ni executar-lo
dins la consola de Docker. Però això en alguns sistemes no funciona bé per defecte
(p.ex. a Windows dona error perquè falten llibreries). Per tal de tenir entorns
de desenvolupament consistents, en aquest cas el Dockerfile inclou els paquets
necessaris per garantir que dins la consola del contenidor sempre funcioni bé
independentment del sistema operatiu que tinguis.

I pel que fa als textos del tercer tipus, el C, son textos que gestioneu via web
a través dels panells d'administració, ja sigui el panell de Wagtail (per la web)
o el panell d'admin de Django (per l'app de gestió de documents).

### 4.3 Canvis al codi font: format i testeig

#### Format i linting

A la carpeta arrel del projecte (sense entrar a la consola del contenidor) has
d'executar `ruff`.

Aquests són alguns exemples de mostra, la resta d'informació cal consultar-la a
la documentació de Ruff:

    poetry run ruff check .
    poetry run ruff check --fix .
    poetry run ruff check --fix --unsafe-fixes .
    poetry run ruff format .

#### Testeig

Una part de l'aplicació es testeja amb tests unitaris i l'altra amb un test de
navegació fent servir Selenium.

Per executar els tests cal accedir a la consola del contenidor de docker i
executar:

    python manage.py test

**Nota:** Hi ha un test que dona aquest error:

    RuntimeError: Model class srv.apps.web.models.about_us.AboutUsPage doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS

Sospitem que pot tenir a veure amb els tests que incorpori Wagtail, però no ho hem pogut investigar.
