# Veille CI/CD
---------------

## Mission 1 : Comprendre CI/CD :

### 1. Qu'est-ce que la CI (Continuous Integration) ?
- Quels problèmes résout-elle ?
     La CI permet de résoudre les problèmes qui interviennent lors du véveloppement simultané de nombreuses partie/branche d'application potentiellement conflictuelles. Elle va notamment permettre d'effectuer de nombreux test automatisé unitaires et d'intégration necessaire à la bonne intégration du nouveau code dans l'ancien. Ainsi l'identification et la correction de bug est plus rapide est régulière.
- Quels sont les principes clés ?
    Les tests automatisé, l'identification et la correction rapide et facilité des potentiel bug, et une plus grande régularité.
- Donnez 3 exemples d'outils CI
    GitHub Action, GitLab CI/CD, Avure DevOps

### 2. Qu'est ce que le CD (Continuous Deployment/Delivery)
- Différence entre Continuous Delivery et Continuous Deployment ?
    Le continuous Delivery désigne le processus qui permets l'automatisation de la publication du code validé (via la CI) dans un référentiel où l'équipe d'exploitation pourra déployer rapidement l'application en production. Le Continuous Deployment lui va plus loin, il automatise en effet directement la mise en production du code validé où il pourra être utilisé par des clients.
- Quels sont les risques et bénéfices ?
    Le Continuous Delivery comporte moin de risque étant donné que le code passe par l'équipe d'exploitation ou les équipes métiers. Le code peut donc ête revérifié avant d'être mis en produciton, son avantage principale est qu'il pallie le manque de visibilité et de communication entre les équipe de dev et les équipes métiers. Cela permets aussi aux équipes d'exploitation de disposer d'un code base déployable à tout moment en production nécessitant le moin d'efforts possible.
    Le continuous Deployement permets quand à lui de décharger les équipes d'exploitation des processus manuels qui ralentissent la distribution des applications. En revanche aucun contrôle n'intervient à l'étape précédent la mise en production, ce type de déploiement nécessite donc un investissement inital conséquent pour permettre l'automatisation de beaucoup de test avant la mise en prod.

### 3. Pet necessiteourquoi le CI/CD est important ?
- Impact sur la qualité du code : En effet, le code subit de nombreux test à chaque étape.
- Impact sur la vitesse de développement : En effet, ces pratique permettent une plus grande régularité d'intégration du code et donc une meilleure intégration des commentaires utilisateurs. Il est en effet plus facile de développer et distribuer des petites modif l'une après l'autre.
- Impact sur la collaboration en équipe : En effet, les équipes de dev et métiers subissent souvent un manque de communication et de visibilité, avec le CI/CD on obtient un code deployable plus facilement.


## Mission 2 : Maîtriser uv :

### 1. Qu'est ce que uv ?
*Uv est un gestionnaire de paquet et un installateur Python moderne écrit en Rust*
- En quoi est-ce différent de pip/poetry/pipenv ? Et quels sont les avantages ?
    Uv est plus rapide pour l'installation de paquer et la résolution des dépendances. UV combine la création d'environnement et la gestion des paquets en un seul outil. UV fournis aussi des messages d'erreurs plus clair et une meilleure résolution des conflits liés aux dépendances. UV possède de même une très bonne reproductibilité garantissant des environnements cohétrent entre différents système. Enfin UV utilise nettement moin de mémoire en plus de meilleures performance.

### 2. Comment uv fonctionne avec pyproject.toml ?
- Structure du fichier : Ce fichier est le coeur du projet. Il contient le nom, la version, la description, le nom du readme, la version de python nécessaire, une liste des dépendances etc...
- Gestion des dépendances (séparé par sections) : On peut séparer les dépendances par section et uv va pouvoir savoir qu'est ce qui est nécessaire ou non à télécharger selon le contexte
- Build backend : pyproject.toml permet notamment le respect des stadards dans python, pour le build backend c'est le standard pep 517, en déclarant un build backend dans le pyproject.toml on simplifie la création de package et aussi plus tard l'insatalation du package

### 3. Comment utiliser uv dans GitHub Actions
- Intallation : astral-sh/setup-uv :
                                  - name: Install uv
                                    uses: astral-sh/setup-uv@v7
- Cache des dépendances : Ca permet de faire persister les package pour les réutiliser à chaque construction et éviter de le refaire à chaque fois.
- Exécution de commandes : UV permets l'utilisation de commandes, que l'on peut exécuter dans le cli.


## Mission 3 : Comprendre Semantic Release :
### 1. Qu'est-ce que le versionnage sémantique (SemVer) ?
*Python Semantic Release permets d'automatiser les mécanisme de publication. Ainsi il permet de parser les commits et d'automatiquement choisir les numéros de version.*
- Format MAJOR.MINOR.PATCH & quand bumper chaque niveau :
        PATCH : un commit de type `fix`, correction d'un bug dans le code
        MINOR : un commit de type `feat`, introduction d'une nouvelle fonctionalité dans le code
        MAJOR : un commit de type `BREAKING CHANGE`, introduit une rupture de compatibilité dans l'API.

### 2. Qu'est ce Conventional Commits ?
- Format des messages : Le format des messages est important
- Type de commits : git commit -m"<type>(<optional scope>): <description>" \
- Impact sur le versionnage : selon le <type> ça impact un chiffre différent du versionnage : "MAJOR.MINOR.PATCH" --> "BREAKING CHANGE/!.feat.fix" --> 0.1.5

### 3. Comment python-semantic-release fonctionne ?
- Configuration dans pyproject.toml : Par défaut il y a une configuration, mais on peut la modifier dans une table TOML `[tool.semantic_release]`
- Génération du CHANGELOG : Grâce  automatiquement soit une description entre deux commits
- Création des releases GitHub : `build(release): bump version to 1.0.0`


## Mission 4 : Comparatif d'outils :
### Comparez Ruff, Flake8, Pylint :
- Ce sont des outils qui garantissent la qualité du code. Flake8 permet de détecter les erreurs et violations de style, Pylint permet une analyse plus approfondie. Ruff combine tous les outils en un seul il est écrit en Rust et est donc bien plus rapide.


### Formatters Python — Ruff format, Black, autopep8 :
*Les formatters permettent d’uniformiser automatiquement le style du code selon des conventions définies.*
- Ruff format est très rapide et compatible avec Black, permet d’avoir linter + formatter dans un seul outil.
- Black : déjà dans l’écosystème Python, très adopté mais peu configurable (opinionated).
- autopep8 : plus permissif et configurable mais moins cohérent dans le rendu final.
Ruff format est plus performant et la simplification de la stack (Black reste valable).

---

### Type Checkers — Mypy, Pyright, Pyre :
*Les type checkers permettent de vérifier statiquement les types Python pour éviter des erreurs à l’exécution.*
- Mypy : référence historique avec une grande communauté et une très bonne précision.
- Pyright : très rapide avec excellente intégration IDE (VS Code).
- Pyre : performant et utilisé dans de grandes entreprises mais moins populaire.
Pyright est mieux pour sa vitesse et son intégration moderne.

---

### Frameworks de Tests — pytest, unittest :
*Les frameworks de tests permettent d’automatiser la validation du code.*
- pytest : syntaxe simple, assertions naturelles, système de fixtures puissant et énorme écosystème de plugins.
- unittest : inclus dans la standard library Python mais plus verbeux et moins flexible.
pytest pour la productivité et la flexibilité.

---

### Security Scanners — Bandit, Safety, Snyk, Trivy (optionnel) :
*Les outils de sécurité permettent de détecter les vulnérabilités dans le code ou les dépendances.*
- Bandit : analyse statique du code Python, gratuit mais peut générer des faux positifs.
- Safety : détecte les vulnérabilités dans les dépendances Python uniquement.
- Snyk : solution commerciale très complète (code, dépendances, containers).
- Trivy : excellent pour l’analyse de containers et infrastructures.
Open source : Bandit + Safety

---

## Tableau comparatif :

Outil | Catégorie | Avantages | Inconvénients | Note /10 | Choix ?
------|-----------|-----------|--------------|----------|--------
Ruff | Linter | Ultra rapide, tout-en-un | Moins profond que Pylint | 9.5 | ✅
Flake8 | Linter | Stable, plugins nombreux | Plus lent, config fragmentée | 7.5 | ❌
Pylint | Linter | Analyse très complète | Lent, complexe | 8 | ❌
Ruff format | Formatter | Très rapide, intégré Ruff | Adoption plus récente | 9 | ✅
Black | Formatter | Standard industrie | Peu configurable | 9 | ✅ (alt)
autopep8 | Formatter | Flexible | Résultat moins homogène | 6.5 | ❌
Pyright | Type checker | Très rapide, IDE excellent | Moins historique que Mypy | 9.5 | ✅
Mypy | Type checker | Référence, précis | Plus lent | 9 | ✅ (alt)
Pyre | Type checker | Très performant | Peu adopté | 7 | ❌
pytest | Tests | Flexible, plugins, simple | Dépendance externe | 10 | ✅
unittest | Tests | Standard library | Verbeux | 6.5 | ❌
Bandit | Security | Gratuit, Python natif | Faux positifs | 8 | ✅
Safety | Security | Dépendances vulnérables | Limité | 8 | ✅
Snyk | Security | Très complet | Payant | 9 | ✅ (entreprise)
Trivy | Security | Containers excellent | Moins Python pur | 8 | ✅ (DevOps)


## Mission 5 : Comparatif d'outils :

### 1. Comment MkDocs génère de la documentation ?
*MkDocs est un générateur de site statique spécialisé pour la documentation de projets. Les fichiers sources sont écrits en Markdown puis transformés en site HTML statique.*
- Le fonctionnement repose sur :
        - Des fichiers `.md` contenant la documentation
        - Un fichier de configuration `mkdocs.yml`
        - Un thème graphique (par exemple :contentReference[oaicite:1]{index=1})
- MkDocs possède un serveur de développement intégré permettant de prévisualiser la documentation en temps réel avec rechargement automatique.
- Le résultat final est un site statique qui peut être hébergé partout (GitHub Pages, serveur web, cloud…). :contentReference[oaicite:2]{index=2}

### 2. Comment déployer sur GitHub Pages ?
*GitHub Pages permet d’héberger un site web directement depuis un dépôt GitHub.*
- Le principe :
        - Le site est généré localement (ex : `mkdocs build`)
        - Les fichiers sont publiés dans une branche spécifique (souvent `gh-pages`) ou via un workflow GitHub Actions
        - GitHub publie automatiquement le site sur une URL publique
- Il est possible d’utiliser un domaine personnalisé et HTTPS.
- GitHub Pages peut être configuré pour publier automatiquement à chaque push sur une branche donnée. :contentReference[oaicite:4]{index=4}


### 3. Qu'est-ce que mkdocstrings ?
*mkdocstrings est un plugin MkDocs permettant de générer automatiquement de la documentation API à partir du code source (docstrings Python).*
- Il s’intègre dans MkDocs via la configuration et permet :
        - D’extraire les docstrings directement du code
        - De maintenir une documentation synchronisée avec le projet
        - D’éviter la duplication entre code et documentation
- Il fonctionne particulièrement bien avec Material for MkDocs qui propose des composants visuels avancés pour afficher la documentation technique. :contentReference[oaicite:5]{index=5}
