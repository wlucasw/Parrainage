# Parrainage

### Principe de fonctionnement :

  L'algorithme commence par ranger les parrains et les fillots de plus difficile au plus facile à matché (mesurer par la moyenne du LoveScore), à chaque parrains on associe un fillots, on regroupe les fillots par familles et on écrit les match dans un Excel.
  A noter : bien qu'il y ait des familles les matchs sont font individu par individu.
  Les matchs sont fait de telle sorte à ce que tout le monde soit associé à un partenaire pas trop mauvais. On définie qu'un match est bon si le LoveScore est bas. On calcul le LoveScore en comparant les réponses aux questionnaires, plus les réponses sont éloignées plus on rajoute au LoveScore. Pour une question on rajoute plus de points au LoveScore plus la pondération de la question est importante.

### Changement à faire :

  Dans l'absolu presque tout peut être garder tel quel et ça marchera. Cependant, si le form est modifié, il faut naturellement changer la partie lecture de réponse et la partie Lovescore.

### Problèmes rencontrés :

  Le plus gros problème auquelle je me suis heurté est le fait que j'avais plus de fillots que de parrains donc j'ai dû rajouter des "parrains fantômes", c'est à dire que j'ai dédoublé un parrains par famille pour pouvoir leur donner deux fillots. Avec les dernières améliorations, on dédouble un parrains par famille tant qu'il n'y en a pas assez.
  J'avais tenté de rajouter des estimation de Lovescore entre tous les parrains et tous les fillots et pas juste le parrains associé mais les résultats n'étaient pas très concluant.

### Point à améliorer :

  La pondération peut toujours être améliorer. On constate nottament que les questions sur les "ters" est peut être trop pondéré.
  D'autre part on constate une grande différence entre les EI1 et les EI2 niveau estimation de la consommation d'alcool (voir form).
  
  
### Lien

Lien du drive avec le form : https://drive.google.com/drive/folders/129CfRi_36QOkDQ7FuoclgIY9VYtQA0gB?usp=sharing
Lien du drive de passation de Sylvain Fox : https://drive.google.com/drive/folders/1DJlrysmoKMvxw-zt983U7WHCANtDRziE?usp=sharing
