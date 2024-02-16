# Projet ARP : Accessibilité dans Z²
## Membres du Groupe

- Eldis YMERAJ
- Tolgan SUNER

## Aperçu du Projet

Dans le cadre de notre unité d'enseignement ARP, nous avons abordé un problème de recherche complexe : l'accessibilité dans \( \mathbb{Z}^2 \), un défi qui a pris des années à résoudre. Ce projet visait à implémenter différentes heuristiques et à tester diverses approches pour explorer des solutions potentielles, représentées ensuite sous forme de graphiques.

### Développement et Méthodologie

Nous avons développé notre projet en Python, en nous concentrant sur :

- **Implémentation d'heuristiques** : Exploration de diverses stratégies pour naviguer dans l'espace des solutions.
- **Analyse graphique** : Représentation des résultats de nos expérimentations sous forme de graphiques pour une meilleure compréhension des performances des heuristiques.

### Objectifs et Résultats

Le but était de comprendre en profondeur les défis liés au problème d'accessibilité dans \( \mathbb{Z}^2 \) et de mettre en évidence l'efficacité relative des différentes heuristiques testées. Nos résultats ont permis d'illustrer comment certaines approches peuvent significativement améliorer la recherche de solutions.

## Technologies Utilisées

- **Python** : Pour le développement des algorithmes et la manipulation des données.
- **Librairies Python** : Utilisées pour la création de graphiques et l'analyse des performances des heuristiques.

## Conclusion

Ce projet a non seulement renforcé notre compréhension des problèmes d'accessibilité dans des espaces discrets mais a également démontré la puissance des heuristiques dans la résolution de problèmes complexes. Les visualisations graphiques ont joué un rôle clé dans l'analyse de nos approches et la démonstration de leur efficacité.


# Heuristique

En haut du programme, nous trouvons un dictionnaire permettant de choisir les heuristiques que l'on veut utiliser pour guider la recherche.

```
heuri = {"heuri_accessibilite": True, "heuri_distance": True, "heuri_score": False, "heuri_borne": False}
```

1. **heuri_accessibilite** : permet de savoir si le chemin est accessible. Peut être utilisé avec les autres.
2. **heuri_distance** : permet d'orienter le parcours de l'arbre en fonction de la distance avec le but. Ne peut pas être utilisé avec heuri_score (même si rien ne l'empêche).
3. **heuri_score** : permet d'orienter le parcours de l'arbre en fonction du rapport entre la distance et la profondeur. Ne peut pas être utilisé avec heuri_distance (même si rien ne l'empêche).
4. **heuri_borne** : permet de rechercher dans un espace restreint. Ne peut être utilisé dans des dimensions d'espace différentes de 2. (Il est un peu compliqué de généraliser l'espace de recherche comme le carré, cube, hypercube de même pour la bande de recherche, cylindre, hypercylindre).

# Configuration

Vers la fin du programme, on retrouve les vecteurs initial, action et but. Ceux commentés ont servi pour les résultats présentés dans le rapport. 
Il est possible de tester ses propres jeux de vecteurs en respectant la structure.
J'ai implémenté `but_gen(dim, min_val=None, max_val=None)` et `vecteur_gen(nb_Vecteur, dim, min_val=None, max_val=None)` afin de tester rapidement différentes configurations.

- **dim** : représente la dimension.
- **min_val** : représente le minimum que l'on souhaite pour tous les composants du vecteur.
- **max_val** : représente le maximum que l'on souhaite pour toutes les composantes du vecteur.

Et dans `vecteur_gen()`, on a aussi le nombre de vecteurs qui représentent nos actions.

Le programme a été conçu pour fonctionner dans toute dimension de \(Z\) sauf pour l'heuristique bornée. Cependant, trop peu de tests ont été effectués pour être certain des résultats. On peut remarquer que l'exploration est très longue.
(Penser à mettre un but initial de la bonne dimension)
