# RSI-projekt
Rozproszone wyciąganie cech z obrazów

Klasa Properties powinna być w sumie podzielona na 3 odddzielne pliki, z których każdy by implementował 
jakiś interfejs typu "Trait". Nad tym powinna zostać zbudowana klasa, która sobie stworzy obiekty i poda
im ścieżkę do folderu ze zdjęciami.
Na pierwszym weźle stworzona powinna zostać kilkukrotnie lista plików (żeby nie było za duże na raz) i sukcesywnie przez MPI przesyłana na kolejne węzły.
 
Na węzłach wyszukiwane będą zaimplementowane Cechy a potem wrzucane na 1. węzeł, agregowane i zwracany wynik:

Cechy:
1. Średnia jasność - wyciąganie V z HSV z każdego piksela i liczenie średniej po wyszystkich pikselach na wszystkich zdjęciach.
2. Średnia dynamika - znowu V z HSV, ale tym razem delta pomiędzy 2 następnymi "klatkami".
3. Dominujący kolor - ograniczenie się do H z HSV, dzielenie koła Hue na 8 podgrup i przypisywanie każdego piksela do każdej z nich.
W przypadku 3. pewnie powinno to zostać jeszcze inaczej rozwiązane - metoda trait_cośtam powinna zwracać listę, ponieważ dopiero ta lista powinna być na pierwszym węźle oceniona.
