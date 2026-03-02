# Veille & Concepts

## 1. La différence entre monitoring vs observabilité

**L'observabilité et le monitoring sont étroitement liés.**

- Le monitoring se focalise essentiellement sur des métriques et des seuils prédéfinis pour faire le suivi de l'état de santé et des performances d'un système. Il est réactif, ce qui signifie qu'il identifie les problèmes après qu'ils aient eu lieu.

    > Le monitoring vous informe quand il y a un problème. Il consiste à surveiller les données système et à réagir aux problèmes qu'elles indiquent. Les outils de monitoring surveillent la télémétrie de vos systèmes et peuvent être utilisés pour visualiser les informations et définir les alertes sur les métriques ; par exemple : le débit réseau, l'utilisation des ressources, le stockage disponible et les taux d'erreur. Les logs peuvent également montrer au personnel TI le contexte des problèmes signalés par les outils de monitoring. Toutefois, sans analyse supplémentaire, il peut être difficile de prédire les occurrences futures en se basant seulement sur les données monitorées.
- L'observabilité va au‑delà du monitoring en vous permettant d'inférer l'état interne d'un système en fonction de ses sorties, comme les logs, les métriques et les traces. Elle est proactive et vous permet d'identifier et de gérer les problèmes avant qu'ils n'impactent les utilisateurs.

    >L'observabilité place les pratiques de monitoring au niveau supérieur en révélant la cause et la raison des problèmes ainsi que la façon dont ils se produisent sur tout le stack technologique. L'observabilité digère et analyse les métriques et événements monitorés ainsi que les logs, traces et autres entrants en utilisant des méthodes d'intelligence artificielle (IA), telles que l'apprentissage machine. Ensemble, ces processus d'observabilité produisent des informations détaillées et exploitables sur des problèmes système. Certains services d'observabilité prédisent les problèmes et recommandent ou créent les outils d'automatisation pour les résoudre avant qu'ils n'atteignent les clients.

<br>
<br>

Catégories | Monitoring | Observabilité |
-----------|----------- |---------------
Focus | Passé : ce qui s'est passé. Réactif. | Prédiction : pourquoi et comment cela s'est-il passé et apporte des informations détaillées sur les problèmes futurs potentiels. Proactive.
Résolution des problèmes | Limitée. Elle exige la corrélation des données et l'analyse par le personnel. | Extensive. Elle utilise l'AIOps pour corréler et analyser d'immenses jeux de données afin de fournir des informations détaillées.
Sources de données | Métriques et logs | Métriques, événements, logs et traces (MELT), plus des informations provenant de l'APM, de la sécurité et de la gestion des informations sur les événements (SEIM), du DEM et du RUM.
Efficacité | Limitée par la complexité des systèmes. Les grands jeux de données sur les infrastructures distribuées limitent la rapidité de l'analyse humaine. | Illimitée avec l'AIOps et l'apprentissage machine pour traiter les grands flux de données sur l'infrastructure en temps réel tout en continuant à apprendre de ces données.


## 2. Les trois pilliers de l'observabilité :
Les indicateurs, les logs et les traces sont largement reconnus comme les trois piliers fondamentaux de l’observabilité

### Que sont les indicateurs ? (Ou, que se passe-t-il ?)
*Les indicateurs sont les données numériques brutes collectées à partir de diverses sources, telles que le matériel, les applications et les sites Web, qui mesurent les éléments connus. Ils fournissent des informations sur l'utilisation des ressources, les performances et le comportement des utilisateurs.*
Les types d’indicateurs sont les suivants :
* **Indicateurs de l’hôte :** utilisation de la mémoire, du disque et du processeur
* **Indicateurs de performance réseau :** temps de fonctionnement, latence, débit
* **Indicateurs applicatifs :** temps de réponse, taux de requêtes et d’erreurs
* **Indicateurs du pool de serveurs :** total des instances, nombre d’instances en cours d’exécution
* **Indicateurs de dépendances externes :** disponibilité, état du service

### Que sont les logs ? (Pourquoi cela se passe-t-il ?) :
*Les logs sont des données structurées et données non structurées provenant de votre infrastructure, de vos applications, de vos réseaux et de vos systèmes. Ils sont constitués d'entrées horodatées relatives à des événements spécifiques.*
Différents types d'appareils et de systèmes émettent des logs :
* Les dispositifs réseau
* Les systèmes d'exploitation
* Les applications
* Les appareils IoT
* Applications tierces

### Que sont les traces ? (Où cela se passe-t-il ?)
*Les traces, qui combinent certains aspects des indicateurs et des logs, permettent de cartographier les données à travers les différents composants réseau pour visualiser le workflow d’une requête. Elles représentent le parcours complet d’une requête à travers le réseau, capturant le chemin emprunté et la durée de vie de chaque composant impliqué dans le traitement de cette requête. En résumé, le traçage aide les ingénieurs en fiabilité des sites (SRE) et les équipes de développement logiciel à comprendre le « où » et le « comment » des événements et des problèmes système.*
Les données de suivi peuvent inclure :
* La durée des événements et des opérations réseau
* Le flux des paquets de données dans l’architecture
* L'ordre dans lequel les requêtes traversent les services réseau
* La cause racine des erreurs système


## 3. L'architecture pull de Prometheus :
Le modèle de collecte de Prometheus utilise le pull (ou scrapping) pour interroger les cibles à travers leurs points de terminaison d'exposition (endpoints) pour extraire les métriques. Cette méthode est différente des systèmes basés sur le push, dans lesquels les clients envoient leurs données à un collecteur central. Le scrapping permet une configuration plus souple et une découverte dynamique des services.


## 4. Les 4 types de métriques (Counter, Gauge, Histogram, Summary)
*Une métrique est un triplet : un nom, un ensemble de labels et une valeur numérique, le tout associé à un timestamp.*

Composant | Rôle | Exemple
----------|----- |---------------
Nom	| Identifie ce qu’on mesure	| http_requests_total
Labels	| Dimensionnent la métrique (paires clé/valeur)	| method="GET", status="200"
Valeur	| Le chiffre mesuré	| 142857
Timestamp	| Quand la mesure a été prise	| (implicite, ajouté à la collecte)

### Analogie du compteut de voiture :
>Le tableau de bord d’une voiture est un système de métriques :
Le compteur kilométrique ne fait que monter — c’est un counter.
L’indicateur de vitesse monte et descend en temps réel — c’est un gauge.
La répartition des trajets par durée (combien de trajets de 0-10 min, 10-30 min, 30+ min) — c’est un histogram.

*Les systèmes de monitoring modernes (Prometheus, OpenTelemetry, StatsD) distinguent 4 types fondamentaux de métriques. Chacun répond à un besoin précis. Choisir le mauvais type revient à mesurer la température avec un compteur kilométrique.*

### Counter (compteur)
Un counter est un compteur monotone croissant : il ne fait que monter (ou revenir à zéro quand le processus redémarre). On ne regarde jamais sa valeur brute — on calcule son taux de variation dans le temps.
**Quand l’utiliser :** tout ce qui s’accumule de façon irréversible.
**Ce qu’on en tire :** le taux par seconde. “Combien de requêtes par seconde mon service traite-t-il en ce moment ?” s’obtient en calculant la variation du counter sur un intervalle :
```
Concept : rate(http_requests_total, sur 5 minutes)
→ "en moyenne, X requêtes/seconde sur les 5 dernières minutes"
```

### Gauge (jauge)
Un gauge est une valeur qui monte et descend librement. Il représente un état instantané, une “photo” à un instant donné.
**Quand l’utiliser :** tout ce qui reflète un état courant.
**Ce qu’on en tire :** la valeur courante, les min/max, les tendances. “La file d’attente est-elle en train de grossir ?” → on regarde le gauge au fil du temps.
*Le pourcentage de CPU est un cas particulier : il est exposé sous forme de counter (node_cpu_seconds_total) et c’est le calcul rate() qui produit un pourcentage. Ce n’est pas un gauge natif, mais le résultat affiché sur un dashboard se comporte comme un gauge (il monte et descend).*

### Histogram (histogramme)
Un histogram mesure la distribution des valeurs observées en les répartissant dans des buckets (intervalles) prédéfinis. Il est conçu pour répondre à la question : “Quel pourcentage de mes requêtes prennent moins de 300 ms ?”
**Quand l’utiliser :** latence, taille de requête, durée d’opération — tout ce qui a une distribution avec des percentiles intéressants.
**Comment ça marche :** vous définissez des seuils (buckets), par exemple : 0,01s, 0,05s, 0,1s, 0,25s, 0,5s, 1s, 5s. L’histogram incrémente le compteur de chaque bucket où la valeur observée “rentre”. Une requête de 0,3s incrémente les buckets 0,5s, 1s et 5s (tous les buckets supérieurs ou égaux à la valeur).

Le système stocke en réalité 3 séries par histogram :

* `_bucket{le="0.5"}` : nombre d’observations ≤ 0,5 s
* `_sum` : somme de toutes les valeurs observées
* `_count` : nombre total d’observations

À partir de ces données, on peut calculer des percentiles (p50, p95, p99) côté serveur, sans connaître chaque valeur individuelle. En Prometheus, vous requêtez `..._bucket`, `..._sum` et `..._count` — le nom racine (`http_request_duration_seconds`) est une famille de séries, pas une série unique.

### Summary (résumé) :
Un summary ressemble à un histogram, mais les percentiles sont calculés côté client (dans l’application) au lieu du côté serveur.

Critère	| Histogram	| Summary
--------|-----------|----------
Calcul des percentiles	| Côté serveur (à la requête)	| Côté client (dans l’application)
Agrégation entre instances	| Possible (sum des buckets)	| Impossible (les percentiles ne s’agrègent pas)
Précision	| Approximation (dépend des buckets)	| Plus directe (côté client), dépend de l’implémentation
Coût en séries temporelles	| 1 série par bucket	| 1 série par quantile
Recommandation	| Préféré dans la plupart des cas	| Si vous savez exactement quels quantiles vous voulez, et que vous n’avez pas besoin d’agréger


## Le rôle de Grafana :
Grafana est votre cockpit d'observabilité : vous branchez des sources de données (métriques / logs / traces) et vous obtenez des dashboards lisibles, une exploration ad-hoc et des alertes.
Grafana ne stocke pas : il interroge des backends (Prometheus, Loki, Tempo, etc.)
