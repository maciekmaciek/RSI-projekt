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

Ad 3.
tablica 'colors' zawiera w sobie pary zakres - kolor.
Każdy kolor ma zakres o dlugosci 0.125 i colors[0] zawiera srodek tego przedzialu - red = [0,0625; 0,1775) itd.Metoda assign_pixel_to_color przyjmuje trójke kolorów (red,green,blue), zamienia j
 na hsv i bierze H. w returnie H z przedziau [0-1] zamieniane jest na {0, 1, 2,..., 8}. dominating_image_colors zwieksza po prostu licznik danej komórki tabeli odpowiadajcej kolorom.
 
 Wlasciwie mozna to tak zostawic i zmienic tylko return w trait_dominating_color, zeby zwracal tablice z wynikami a nie stringa i dopiero w ostatnim wezle to na stringa zmienic
