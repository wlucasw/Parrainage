# Parrainage 

## Algorithme :

### Principe de fonctionnement :

  L'algorithme commence par ranger les parrains et les fillots du plus difficile au plus facile à matcher (mesuré par la moyenne du LoveScore), à chaque parrain on associe un fillot, on regroupe les fillots par famille et on écrit les matchs dans un Excel.
  À noter : bien qu'il y ait des familles les matchs sont font individu par individu.
  Les matchs sont faits de telle sorte à ce que tout le monde soit associé à un partenaire pas trop mauvais. On définit qu'un match est bon si le LoveScore est bas. On calcule le LoveScore en comparant les réponses aux questionnaires, plus les réponses sont éloignées plus on rajoute au LoveScore. Pour une question on rajoute plus de points au LoveScore plus la pondération de la question est importante.

### Changement à faire :

  Dans l'absolu presque tout peut être gardé tel quel et ça marchera. Cependant, si le form est modifié, il faut naturellement changer la partie lecture de réponse et la partie Lovescore.

### Problèmes rencontrés :

  Le plus gros problème auquel je me suis heurté est le fait que j'avais plus de fillots que de parrains donc j'ai dû rajouter des "parrains fantômes", c'est à dire que j'ai dédoublé un parrains par famille pour pouvoir leur donner deux fillots. Avec les dernières améliorations, on dédouble un parrain par famille tant qu'il n'y en a pas assez.
  J'avais tenté de rajouter des estimations de Lovescore entre tous les parrains et tous les fillots et pas juste le parrains associés mais les résultats n'étaient pas très concluants.

### Points à améliorer :

  La pondération peut toujours être améliorée. On constate notamment que les questions sur les "ters" sont peut-être trop pondérées.
  D'autre part on constate une grande différence entre les EI1 et les EI2 niveau estimation de la consommation d'alcool (voir form).
  On constate parfois un phénomène d'hétérogénéité entre les fillots important quand les parrains ont des réponses trop différentes.
  Certaines familles se sont retrouvées avec presque que des fillots étrangers, ce n'est pas nécessairement un problème mais c'est à noter.
  
## Form et excel :

### Principe de fonctionnement :

  On envoie un form avec quasiment les mêmes questions aux EI1(le plus tôt possible à la rentrée) et aux EI2 (avant les grandes vacances). On peut modifier la formulation des questions entre les deux forms (ex : "Tu bois ?" se transforme en "Tu comptes boire ?" pour les EI1) mais les réponses à choix multiples doivent rester les mêmes. J'avais rajouté deux questions pour les EI2 : "le nom de leur famille ?", "l'objet qu'ils comptent apporter ?".
  
### Regrouper les gens par familles :

  Deux méthodes ont été envisagées et mises en place : 
    - Demander à chaque famille de se nommer et demander à chacun le nom de sa famille.
    - Demander à chacun avec qui il est dans sa famille.
   Le problème de la deuxième méthode est que tu peux avoir des situations type : "A est avec B et C, B est avec A et D et C est avec E" et c'est pas facile à démêler (cf document passation sylvain (2)) mais plus facile à automatiser. La première solution evite le problème précédemment mentionné mais rend l'automatisation plus complexe car aucun putain de connard n'écrit le nom de sa famille pareil. Un système à base de ILIKE comme en SQL peut être envisagé mais en ce qui me concerne j'ai regroupé à la main les gens en famille dans une feuille de l'Excel. 
   On avait fixé un nombre maximum de personnes par famille (max 6) voir si c'est nescessaire ou pas (ça évite au moins d'avoir des familles à 15 ce qui est peut-être pas opti).
   
### Problèmes rencontrés :
  
  Les trolls : surtout les EI2 qui répondent deux fois avec une réponse full bullshit -> réponse à éliminer
  Les EI2 qui répondent au dernier moment.
  Les familles incomplètes à 2 jours de la soirée de Parrainage.
  Les gens qui ne mettent que leur nom ou que leur prénom (ex : formulaire au nom de "Lucas").
  Les gens qui envoient deux fois le questionnaire.
  
## Liens

(1) Lien du drive avec le form : https://drive.google.com/drive/folders/129CfRi_36QOkDQ7FuoclgIY9VYtQA0gB?usp=sharing
(2) Lien du drive de passation de Sylvain Fox : https://drive.google.com/drive/folders/1DJlrysmoKMvxw-zt983U7WHCANtDRziE?usp=sharing
